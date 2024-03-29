# IoT Live Streaming System for Information Systems Course @NTUA

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Python 3.9](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)


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

Refer to the following documentation for installation instructions:
https://docs.docker.com.xy2401.com/v17.12/compose/install/

### Step 3: Docker compose

Inside the root directory of the project run the following command to start the system:

```
docker-compose up
```

### Step 4: Live Streaming Layer

Requires java 11, jdk.

```
java -jar liveStreamingLayer/flinkExecutable.jar
```

### Step 5: Device Layer

This is the producer of the data of the IoT devices.
Requires python 3, confluent_kafka, numpy, pillow, matplotlib, scipy.

```
python3 deviceLayer/run_producer.py
```

### Step 6: Data Storage Layer - Syncing

This takes the data from the kafka topic and puts it in the hbase database.

```
./dataStorageLayer/sync.sh
```

### Step 7: Websocket Server

This is the server that connects the grafana dashboard to the hbase database. Go to `/dataStorageLayer/websockets_server` and run the following command:

```
npm install
```

and then

```
npm run start
```

### Step 8: Grafana set up

Go to `http://localhost:3000` and log in with the following credentials:

```
admin - admin
```

Then add the datasource with this script:

```
./presentationLayer/import_data_sources.sh
```

and at last import the dashboard from the `presentationLayer` folder, using the grafana GUI, dashboard->import.

## All together

We made and a run-all script that runs all the steps above. It is located in the root directory of the project and is called `post_setup.sh`. It is not recommended to use this script to run the system because of the that processes are not killed when the script is terminated. It is recommended to run the steps above manually.
