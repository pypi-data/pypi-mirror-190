import base64
import json
import os
import time
from typing import Any, Dict, List, Optional, Union, Collection
from uuid import uuid4

import requests


class Client:
    def __init__(self, kafka_rest_api_url: Optional[str] = None, auth_headers: Optional[Dict[str, str]] = None):
        """
        Create a client instance.
        :param kafka_rest_api_url: Kafka REST API URL.
        :param auth_headers: Authentication Headers.
        """
        self.kafka_rest_api_url = os.environ['KAFKA_REST_API_URL'] if not kafka_rest_api_url else kafka_rest_api_url
        self.auth_headers = auth_headers

    def request(self, **kwargs):
        kwargs["url"] = f"{self.kafka_rest_api_url}{kwargs['url']}"
        if self.auth_headers:
            kwargs.get("headers", {}).update(self.auth_headers)

        response = requests.request(**kwargs)

        if not response.ok:
            print(response.content)
            response.raise_for_status()

        return response


class Producer(Client):
    def __init__(self, producer_data_max_size: int = 67_108_864, **kwargs):
        """
        Create a producer instance.
        :param producer_data_max_size: Maximum size of each request payload in bytes.
        :param kwargs:
            kafka_rest_api_url: Provide a Kafka REST Proxy API URL if it is not set as environment variable.
            auth_headers: Optional dictionary of authentication headers.
        """
        super().__init__(kwargs.get("kafka_rest_api_url", ""), kwargs.get("auth_headers"))

        self.max_data_bytes = os.environ.get('PRODUCER_DATA_MAX_SIZE', producer_data_max_size)
        self.key_history, self.key_last_request = [], []

    @staticmethod
    def __manage_keys(len_messages: int, keys: Optional[List[str]] = None):
        if keys:
            try:
                assert len(keys) == len_messages
            except AssertionError:
                raise ValueError("List of keys must have the same size as list of messages.")
            return keys

        return [str(uuid4()) for _ in range(len_messages)]

    def produce(self, messages: Collection, topic: str, keys: Optional[List[str]] = None) -> List[str]:
        """
        Produce messages to a given topic.
        :param messages: JSON serializable Collection of messages.
        :param topic: Corresponding topic.
        :param keys: Optional list of customized keys. Number of keys must match the number of messages.
        :return: List of generated UUID keys.
        """
        headers = {"Content-Type": "application/vnd.kafka.json.v2+json"}
        keys = self.__manage_keys(len(messages), keys)
        records = {"records": [{"key": k, "value": v} for k, v in zip(keys, messages)]}
        record_data = json.dumps(records)

        self._check_data_size(record_data.encode("utf-8"))

        self.request(method="POST", url=f"/topics/{topic}", headers=headers, data=record_data)

        self.key_history.extend(keys)
        self.key_last_request = keys
        return self.key_last_request

    def _check_data_size(self, data: bytes):
        if self.max_data_bytes < len(data):
            raise RuntimeError(f"Producer request data exceeded allowed number bytes: {self.max_data_bytes} bytes")

    def produce_files(self, files: Collection, topic: str, file_max_size: int = 500_000, keys: Optional[List[str]] = None) -> List[str]:
        """
        Produce files to a given topic.
        :param files: List of dictionaries with keys:
                       - name: string with filename.
                       - bytes: bytes.
                       - type: string with type. (optional)
        :param topic: Target topic.
        :param file_max_size: Maximum file size in bytes.
        :param keys: Optional list of customized keys. Number of keys must match the number of messages.
        :return: List of generated UUID keys.
        """

        assert all(
            isinstance(field, str) if field == "name" else (
                field == "bytes" and file[field] <= file_max_size if isinstance(field, bytes) else True)
            for file in files for field in file) is True

        assert all(len(file["bytes"]) for file in files)

        messages = [
            {
                "name": f["name"],
                "bytes": base64.b64encode(f["bytes"]).decode(),
                "type": f["type"]
            } for f in files]

        return self.produce(messages, topic, keys=keys)


class Consumer(Client):
    def __init__(self, **kwargs):
        """
        Create a consumer instance.
        :param kwargs:
            kafka_rest_api_url: Provide a Kafka REST Proxy API URL if it is not set as environment variable.
            auth_headers: Optional dictionary of authentication headers.
            topics: List of topics to consume messages from.
            consumer_group: Assign a consumer group name. Otherwise, assign a randomly generated UUID.
            instance: Assign an instance name. Otherwise, assign a randomly generated UUID.
        """
        super().__init__(kwargs.get("kafka_rest_api_url", ""), kwargs.get("auth_headers"))

        self.created = False

        self.topics = kwargs.get("topics", [])
        self.consumer_group = kwargs.get("consumer_group", str(uuid4()).replace("-", ""))
        self.instance = kwargs.get("instance", str(uuid4()).replace("-", ""))
        self.remaining_keys = set()

    def __enter__(self):
        return self.create().subscribe(self.topics)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def create(self):
        """
        Create a Consumer instance in binary format.
        :return: self.
        """

        if not self.created:
            url = f"/consumers/{self.consumer_group}"
            headers = {"Content-Type": "application/vnd.kafka.json.v2+json"}
            config = json.dumps({"name": self.instance, "format": "binary", "auto.offset.reset": "earliest"})

            response = self.request(method="POST", url=url, headers=headers, data=config)
            self.created = True

        return self

    def subscribe(self, topics: List[str]):
        """
        Subscribe to the given topics.
        :param topics: List of topics to consume messages from.
        :return: self.
        """

        if not topics:
            raise ValueError("No topics to subscribe to.")

        self.topics = topics
        url = f"/consumers/{self.consumer_group}/instances/{self.instance}/subscription"
        headers = {"Content-Type": "application/vnd.kafka.json.v2+json"}
        topics_data = json.dumps({"topics": self.topics})

        r = self.request(method="POST", url=url, headers=headers, data=topics_data)
        return self

    def consume_earliest(self) -> List[Dict[str, Any]]:
        """
        Consume the earliest messages in the assigned topics.
        :return: List of dictionaries where the "value" key contains the message and the "key" key contains its key.
        """
        url = f'/consumers/{self.consumer_group}/instances/{self.instance}/records'
        headers = {'Accept': 'application/vnd.kafka.binary.v2+json'}

        response = self.request(method="GET", url=url, headers=headers, data="")
        response_decoded = [self.decode_record(r) for r in response.json()]

        return response_decoded

    def delete(self):
        """
        Delete the current client instance from the kafka cluster.
        """
        url = f'/consumers/{self.consumer_group}/instances/{self.instance}'
        headers = {'Content-Type': 'application/vnd.kafka.v2+json'}

        self.request(method="DELETE", url=url, headers=headers, data="")
        self.created = False

    def consume(self, keys: List[str], interval_sec: Union[int, float] = 5) -> List[dict]:
        """
        Consume messages from the assigned topics as iterator.
        :param keys: List of keys to choose from the topics.
        :param interval_sec: Minimum interval in seconds between polling requests.
        :return: List of dictionaries where the "value" key contains the message and the "key" key contains its key.
        """

        if interval_sec < 0:
            raise ValueError("'interval_sec' should be an 'int' or 'float' greater or equal to 0.")

        self.remaining_keys = set(keys)

        while self.remaining_keys:
            time.sleep(interval_sec)
            incoming_data = self.consume_earliest()
            data = [d for d in incoming_data if d['key'] in self.remaining_keys]
            yield data
            self.remaining_keys = self.remaining_keys - set(d['key'] for d in incoming_data)

    def consume_all(self, keys: List[str], interval_sec: Union[int, float] = 5) -> List[Dict[str, Any]]:
        """
        Consume all messages from all keys.
        :param keys: List of keys to choose from the topics.
        :param interval_sec: Minimum interval in seconds between polling requests.
        :return: List of dictionaries where the "value" key contains the message and the "key" key contains its key.
        """
        all_data = []

        for data in self.consume(keys, interval_sec):
            all_data.extend(data)

        return all_data

    @staticmethod
    def decode_base64(string: str):
        if string:
            try:
                return json.loads(base64.b64decode(string))
            except json.decoder.JSONDecodeError:
                return base64.b64decode(string)
        return string

    @staticmethod
    def decode_record(record: dict):
        record.update({
            "key": Consumer.decode_base64(record["key"]),
            "value": Consumer.decode_base64(record["value"])
        })

        return record
