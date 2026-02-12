import json
from confluent_kafka import Consumer, KafkaException

TOPIC = "traffic.events"

def main():
    c = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "traffic-consumer-group",
        "auto.offset.reset": "earliest",
    })

    c.subscribe([TOPIC])
    print(f"Consuming from topic: {TOPIC} (Ctrl+C to stop)")

    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            key = msg.key().decode("utf-8") if msg.key() else None
            event = json.loads(msg.value().decode("utf-8"))
            print(f"[RECEIVED] key={key} partition={msg.partition()} offset={msg.offset()} event={event}")

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        c.close()

if __name__ == "__main__":
    main()
