# Flink

## Requirements

- flink-1.16.0

## Run Live Streaming Layer
java -jar YoutPathTo\APS\liveStreamingLayer\flinkExecutable.jar

## Setup in Eclipse IDE

- File > Import... > Select an import wizard > Maven > Existing Maven Project
- Root Directory: "YourPathTo\APS\liveStreamingLayer"
- Select "pom.xml" > Finish
- Run Configurations > JRE > 'Project execution environment JavaSE-11 (jre)'

#### Timestamp : 2022-10-21 00:00

#### Data : 2022-10-20 00:15, 2022-10-20 00:30 … 2022-10-20 23:45, 2022-10-21 00:00 (επομένης)

#### First timestamp for aggregations: 2020-01-02 00:00

## Table with sensor aggs

| Index | Sensor Name | Topic       | Sensor Interval | Required Function                                                                                   |
| ----- | ----------- | ----------- | --------------- | --------------------------------------------------------------------------------------------------- |
| 1     | TH1         | Temperature | 15 min          | AggDay[TH1] = AVG temperature for each sensor                                                       |
| 2     | TH2         | Temperature | 15 min          | AggDay[TH2] = AVG temperature for each sensor                                                       |
| 3     | HVAC1       | Energy      | 15 min          | AggDay[HVAC1] = Sum wh for each sensor                                                              |
| 4     | HVAC2       | Energy      | 15 min          | AggDay[HVAC2] = Sum wh for each sensor                                                              |
| 5     | MiAC1       | Energy      | 15 min          | AggDay[MiAC1] = Sum wh for each sensor                                                              |
| 6     | MiAC2       | Energy      | 15 min          | AggDay[MiAC2] = Sum wh for each sensor                                                              |
| 7     | W1          | Water       | 15 min          | AggDay[W1] = Sum litres of the day for sensor                                                       |
| 8     | Etot        | Energy      | 1 day           | AggDayDiff[Etot] = Diff of value of day with value of previous day                                  |
| 9     | Wtot        | Water       | 1 day           | AggDayDiff[Wtot] = Diff of value of day with value of previous day                                  |
| 10    | Etot        | Energy      | 1 day           | AggDayRest[Etot] = AggDayDiff[Etot] - AggDay[HVAC1] - AggDay[HVAC2] - AggDay[MiAC1] - AggDay[MiAC2] |
| 11    | Wtot        | Water       | 1 day           | AggDayRest[Wtot] = AggDayDiff[Wtot] – AggDay[W1]                                                    |
| 12    | Mov1        | Motion      | Random          | AggDayMov[Mov1] = Sum of movements of the day for the sensor                                        |

# Normal aggragations and data flow.

1. All data, late and normal are accepted by flink and then we sink them to a new kafka topic `raw`.
2. After the aggregations are calculated we filter the late event data, then we sink them to a new kafka topic `aggregated`.
3. The late event data then are sinked to the `late` topic.

# How we handle late events.

The only sensor that produces late events data is the water sensor.

## Late event types.

There are 2 types of late event data.

1. The 2 day late events (accepted).
2. The 10 day late events (rejected).

## Late event flow.

The 2 days late data are normally returned to kafka topic `raw` from flink and we also include them to the aggregations which are sent to the kafka topic `aggragated`.
The 10 days late data are inputted both to a separate kafka topic `late` and the `raw` topic.