import os
import pprint

from kafka_rest.kafka_rest import Consumer, Producer


def main():

    producer_messages = [
        {
            "text": "Genome engineering is a powerful tool for a wide range of applications in biomedical research",
            "algorithm": "TopicRank",
            "n_best": 10
        },
        {
            "text": "Genome engineering is a powerful tool for a wide range of applications in biomedical research",
            "algorithm": "TopicRank",
            "n_best": 5
        }
    ]

    # # Auth Headers

    x_api_key = os.environ['X_API_KEY']
    user_agent = os.environ['USER_AGENT']
    auth_headers = {"x-api-key": x_api_key, "User-Agent": user_agent}

    print("Kafka URL:", os.environ["KAFKA_REST_API_URL"])

    target_topic = "pke"

    # Producer

    print("\n", " Producer ".center(100, "#"), end="\n\n")
    print(f"Send these messages to topic '{target_topic}':", "\n", pprint.pformat(producer_messages, indent=4), "\n")

    producer = Producer(auth_headers=auth_headers)
    new_keys = producer.produce(producer_messages, target_topic)

    print(f"The producer generated these message keys:", "\n", pprint.pformat(new_keys, indent=4))

    # Consumer
    interval_sec = 5

    # Pattern 1 - Instantiation via context manager

    print("\n", " Pattern 1 - Step-by-step instantiation ".center(100, "#"), end="\n\n")

    with Consumer(topics=["pke-response"], auth_headers=auth_headers) as c:
        print(f"Consumer instance '{c.instance}' checks every {interval_sec} second{'s' if interval_sec != 1 else ''}",
              f"and consumes all keys ({', '.join(new_keys)})")
        new_data = c.consume_all(new_keys, interval_sec=interval_sec)

    print("Response Data:", pprint.pformat(new_data, indent=4))

    # ## Pattern 2 - Step-by-step instantiation

    print("\n", " Pattern 2 - Step-by-step instantiation ".center(100, "#"), end="\n\n")

    consumer = Consumer(auth_headers=auth_headers)

    print("Create consumer instance...")
    consumer.create()

    print(f"New consumer instance: '{consumer.instance}'.")

    print(f"Subscribe to topic{'s' if len(target_topic) > 1 and isinstance(target_topic, list) else ''}:",
          f"{', '.join(target_topic) if type(target_topic) in [list, set, tuple] else target_topic}")
    consumer.subscribe(topics=["pke-response"])

    print(f"Produce data to topic '{target_topic}'...")
    keys = producer.produce(producer_messages, target_topic)

    print(f"Consume data every {interval_sec} seconds...")
    consumed_data = consumer.consume_all(keys=keys,
                                         interval_sec=interval_sec)  # or consumer.create().subscribe().consume_all(keys)
    print("Response Data:", "\n", pprint.pformat(consumed_data, indent=4))

    print("Delete consumer to release resources...")
    consumer.delete()

    # ## Pattern 3 - Consumer with iterator

    print("\n", " Pattern 3 - Consumer with iterator ".center(100, "#"), end="\n\n")

    new_keys = producer.produce(producer_messages, target_topic)

    with Consumer(topics=["pke-response"], auth_headers=auth_headers) as consumer:
        print(f"Data from consumer instance '{consumer.instance}'",
              f"(every {interval_sec} second{'s' if interval_sec != 1 else ''}):")

        for i, iter_data in enumerate(consumer.consume(new_keys, interval_sec=1)):
            print(f"Data in iteration {i}:", "\n", pprint.pformat(iter_data, indent=4))

            if iter_data:
                print("Do something with the data...", "\n", "Continue...")
        print("Iteration finished because all keys were processed!")

    print("\n", " Producer with files ".center(100, "#"), end="\n\n")

    file_names = ["test_1.pdf", "test_2.pdf", "test_3.pdf"]

    messages = []
    for name in file_names:
        with open(f"snippet/{name}", "rb") as f:
            messages.append({"name": name, "bytes": f.read(), "type": "application/pdf"})

    target_topic = "pdf2text"

    print(f"Sending files '{', '.join(file_names)}' to topic '{target_topic}'...")

    producer = Producer(auth_headers=auth_headers)
    new_keys = producer.produce_files(messages, target_topic)

    print(f"Consuming responses...")

    with Consumer(topics=[f"{target_topic}-response"], auth_headers=auth_headers) as consumer:
        for i, iter_data in enumerate(consumer.consume(new_keys, interval_sec=1)):
            print(f"Response in iteration {i}:", "\n", pprint.pformat(iter_data, indent=4))

            if iter_data:
                print("Do something with the data...", "\n", "Continue...")
        print("Iteration finished because all keys were processed!")

    print("#" * 100, "\n\n", "-> Snippet finished!")


if __name__ == "__main__":

    main()