![Python](https://img.shields.io/badge/Python-3.x-blue)
![Kafka](https://img.shields.io/badge/Kafka-3.0-orange)
![Docker](https://img.shields.io/badge/Docker-Desktop-blue)

# Traffic Management with Apache Kafka

## Project Description
This project is a technical Big Data project using **Apache Kafka**.  
The objective is to install, configure, and run a Big Data tool and demonstrate its usage with a minimal working example.

The chosen use case is **traffic management**, where different traffic-related events are streamed in real time:
- traffic jams
- road accidents
- speed camera detections

Kafka is used to stream these events, with a Python producer sending data and a Python consumer receiving it.

---

## Chosen Tool
**Apache Kafka**

Kafka is a distributed event streaming platform that allows applications to publish, store, and consume data streams in real time.

---

## Why Kafka
Kafka was chosen because:
- traffic data is continuous and event-based
- Kafka is designed for real-time data ingestion
- producers and consumers are decoupled
- it is commonly used in Big Data architectures

This makes Kafka well suited for a traffic management scenario.

---

## Installation Steps

### Prerequisites
- Windows
- Docker Desktop
- Docker Compose
- Python 3.x


### Step 1 — Start Kafka with Docker Compose
From the project directory:
```bash
docker compose up -d
docker compose ps
```

Kafka runs inside a Docker container and exposes port 9092.

# Proof of execution:

- logs/compose_ps.txt
- logs/kafka_startup.log

### Step 2 — Create the Kafka Topic

A topic named traffic.events is created to store traffic events.
```bash
docker exec -i kafka kafka-topics --bootstrap-server localhost:9092 \
--create --topic traffic.events --partitions 1 --replication-factor 1
```

# Verification:
```bash
docker exec -i kafka kafka-topics --bootstrap-server localhost:9092 --list
docker exec -i kafka kafka-topics --bootstrap-server localhost:9092 \
--describe --topic traffic.events
```

Proof files:

- logs/topics_list.txt
- logs/topic_describe.txt

### Minimal Working Example
# Producer

The producer (producer.py) generates random traffic events:

- TRAFFIC_JAM
- ACCIDENT
- SPEED_CAMERA

Each event is sent as a JSON message to the Kafka topic traffic.events.

### Sample Event JSON:

```json
{
  "event_id": "b137c55c-d83f-4bc4-b9a7-23b77c144897",
  "event_type": "SPEED_CAMERA",
  "ts_utc": "2025-12-20T11:45:25.964046+00:00",
  "city": "Lille",
  "road": "A6",
  "lat": 48.8061,
  "lon": 2.318646,
  "speed_limit_kmh": 70,
  "direction": "N",
  "active": true
}
```
# Consumer

The consumer (consumer.py) subscribes to the same topic and:
- reads messages in real time
- displays the event content
- shows Kafka metadata (partition and offset)

## Running the Example

# Terminal 1 (consumer):
```bash
python src/consumer.py
```

# Terminal 2 (producer):
```bash
python src/producer.py
```

The producer sends events continuously and the consumer receives them immediately.

# Proof logs:

- logs/producer.log
- logs/consumer.log

### Proof of Execution

Execution is proven using log files stored in the logs/ folder:

- Kafka container running
- topic creation and description
- producer sending events
- consumer receiving events

These logs show that the system works correctly end to end.

### Kafka in a Big Data Ecosystem

In a Big Data architecture, Kafka usually acts as the ingestion layer:

- data producers send events to Kafka
- Kafka stores and streams the data
- stream processing tools (Spark, Flink) can process the data
- data can be stored in data lakes or used by dashboards

In this project, Kafka is used as the central streaming component.

### Challenges Encountered

- Docker Desktop was not started, which caused connection errors
  → solved by starting Docker Desktop before running Docker Compose
- The docker-compose file was saved as docker-compose.yml.txt
  → renamed to docker-compose.yml
- Git Bash caused a TTY error with docker exec -it
  → solved by using docker exec -i
- Virtual environment activation was different on Windows
  → used .venv/Scripts/activate instead of Linux paths

### My Setup Notes

This project helped me better understand:

- how Kafka works with Docker
- how producers and consumers communicate
- common setup issues on Windows
- how Kafka fits into a Big Data pipeline

### Project Structure
```

.
├── src/
│   ├── producer.py
│   ├── consumer.py
│   ├── requirements.txt
├── logs/
│   ├── compose_ps.txt  
│   ├── kafka_startup.log
│   ├── topics_list.txt
│   ├── topic_describe.txt
│   ├── producer.log          
│   └── consumer.log    
├── docker-compose.yml    
├── README.md          
```


### Conclusion

This project demonstrates:

- installation and configuration of Apache Kafka
- topic creation and management
- a working producer-consumer pipeline
- Kafka’s role in a Big Data ecosystem




