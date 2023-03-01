# IoT Live Streaming System for Information Systems Course

This is a project for the Information Systems course at the NTUA. The goal of this project is to create a live streaming system for IoT devices. 

## System Architecture

![](assignment/architecture_diagram.png)

The system system's data flow is as follows:

1. Data is generated from a python script immitating a series of IoT devices and gets sent to a Kafka broker.

2. The data is then consumed by an Apache Flink instance which performs a series of aggregation and filtering operations on the data.

3. The data is then sent back to the Kafka broker in appropriate topics. A copy of the original sensor data is also sent to a Kafka topic for later storage.

4. The data present in topics populated by Flink is then consumed by a python script which sends the data to an Apache Hbase instance using the Apache Triton API.

5. A Grafana instance is used to visualize the data stored in the Hbase instance. The data gets transfered using a Node.js Websocket server that periodically queries the Hbase instance.


## Installation

### Step 1: Clone the repository

```bash
$ git clone URL
```

### Step 2: Install Docker and Docker-Compose

Refer 
