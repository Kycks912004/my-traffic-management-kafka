import json
import random
import time
from datetime import datetime, timezone
from uuid import uuid4
from confluent_kafka import Producer

TOPIC = "traffic.events"

EVENT_TYPES = ["TRAFFIC_JAM", "ACCIDENT", "SPEED_CAMERA"]
CITIES = ["Paris", "Lyon", "Marseille", "Lille", "Toulouse"]
ROADS = ["A1", "A6", "A7", "A10", "A13", "Peripherique", "N118"]

def delivery_report(err, msg):
    if err is not None:
        print(f"[DELIVERY ERROR] {err}")
    else:
        print(f"[DELIVERED] topic={msg.topic()} partition={msg.partition()} offset={msg.offset()}")

def make_event():
    event_type = random.choice(EVENT_TYPES)
    base = {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "city": random.choice(CITIES),
        "road": random.choice(ROADS),
        "lat": round(random.uniform(48.80, 48.90), 6),
        "lon": round(random.uniform(2.25, 2.42), 6),
    }

    if event_type == "TRAFFIC_JAM":
        base.update({"severity": random.choice(["LOW", "MEDIUM", "HIGH"]),
                     "avg_speed_kmh": random.randint(5, 35),
                     "length_m": random.randint(200, 5000)})
    elif event_type == "ACCIDENT":
        base.update({"severity": random.choice(["MINOR", "MAJOR"]),
                     "lanes_blocked": random.randint(1, 3),
                     "injuries_reported": random.choice([True, False])})
    else:
        base.update({"speed_limit_kmh": random.choice([30, 50, 70, 90, 110, 130]),
                     "direction": random.choice(["N", "S", "E", "W"]),
                     "active": True})
    return base

def main():
    p = Producer({"bootstrap.servers": "localhost:9092"})
    print(f"Producing to topic: {TOPIC} (Ctrl+C to stop)")

    try:
        while True:
            event = make_event()
            p.produce(
                TOPIC,
                key=event["event_type"].encode("utf-8"),
                value=json.dumps(event).encode("utf-8"),
                callback=delivery_report,
            )
            p.poll(0)
            print("[SENT]", event)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        p.flush(10)

if __name__ == "__main__":
    main()
