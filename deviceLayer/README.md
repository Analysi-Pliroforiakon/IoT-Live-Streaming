# Device Layer

This folder has all code we use to produce the data and send them to a kafka topic.

## Devices

Two sensors for temperature.

- TH1
- TH2

Four electric devices sensors that measure the device energy consumption.

- HVAC1
- HVAC2
- MiAC1
- MiAC2

1 Total energy sensor, measuring for the first day, or the start of the script.

- Etot

1 Water sensor

- W1

1 Total water sensor, measuring for the first day, or the start of the script.

- Wtot

1 Motion sensor that measures the number of movements in an area.

- Mov1

## Devices and kafka topics

In order to make the next layer , live streaming layer easier for the aggregations we used the following topics for each sensor. In order to understand why please read the live streaming layer README.md file. And the aggregation table, in the same file.

| Device | Kafka topic |
| ------ | ----------- |
| TH1    | temperature |
| TH2    | temperature |
| MiAC1  | energy      |
| MiAC2  | energy      |
| HVAC1  | energy      |
| HVAC2  | energy      |
| Etot   | energy      |
| W1     | water       |
| Wtot   | water       |
| Mov1   | motion      |

## Requirements

- python 3
- confluent_kafka
- numpy
- pillow
- matplotlib
- scipy
