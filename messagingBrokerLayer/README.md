# Kafka

## Required packages
- `docker`
- `docker-compose`

## Setup
`docker-compose -f docker-compose.yml up`

## Kafka Manager UI
Access CMAK with a browser using address `localhost:9000`

## Info
Kafka configuration docs
- [Docker Configuration Parameters for Confluent Platform](https://docs.confluent.io/platform/current/installation/docker/config-reference.html#required-zk-settings)
- [Configure Multi-Node Environment
](https://docs.confluent.io/platform/current/kafka/multi-node.html#configure-multi-node-environment)

CMAK-Kafka Manager source: https://github.com/eshepelyuk/cmak-docker

## Topics

| Topic Name  | Sensors-Keys                       | Partition # |
|-------------|------------------------------------|-------------|
| temperature | TH1, TH2                           | 2           |
| energy      | HVAC1, HVAC2,   MiAC1, MiAC2, Etot | 2           |
| motion      | Mov1                               | 2           |
| water       | W1, Wtot                           | 2           |


## Tests
Test scritps:
- `$ python producer_test.py`
- `$ python consumer_test.py`

`kafkacat` utility (needs to be installed):
- list topics: `$ kfkacat -b localhost:9092 -L`
- consume from topic: `$ kafkacat -b localhost:9092 -t test_topic`