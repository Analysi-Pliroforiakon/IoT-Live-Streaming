
# Flink

## Requirements
- flink-1.16.0

## Setup in Eclipse IDE

- File > Import... > Select an import wizard > Maven > Existing Maven Project
- Root Directory: "YourPathTo\APS\liveStreamingLayer\java-flink-kafka"
- Select "pom.xml" > Finish
- Run Configurations > JRE > 'Project execution environment JavaSE-11 (jre)'

#### Timestamp : 2022-10-21 00:00
#### Data : 2022-10-20 00:15, 2022-10-20 00:30 … 2022-10-20 23:45, 2022-10-21 00:00 (επομένης)
#### First timestamp for aggregations: 2020-01-02 00:00

## Table with sensor aggs
|Index|Sensor Name| Topic | Sensor Interval| Required Function|
| ---| --- | --- | --- | ---|
|1 |TH1 | Temperature | 15 min | AggDay[x] = AVG temperature for each sensor |
|2|TH2 | Temperature | 15 min| AggDay[x] = AVG temperature for each sensor | 
|3 | HVAC1| Energy | 15 min | AggDay[x] = Sum wh for each sensor | 
|4 | HVAC2| Energy | 15 min | AggDay[x] = Sum wh for each sensor | 
|5 | MiAc1| Energy | 15 min | AggDay[x] = Sum wh for each sensor|
|6 | MiAc2| Energy | 15 min | AggDay[x] = Sum wh for each sensor|
|7| W1 | Water | 15 min | AggDay[x] = Sum litres of the day for sensor |
|8 | Etot | Energy | 1 day | AggDayDiff[y] = diff of value of day with value of previous day|
|9|Wtot | Water | 1 day | AggDayDiff[y] =  diff of value of day with value of previous day |
|10 | Etot | Energy | 1 day| AggDayRest[Etot] = AggDayDiff[Etot] - AggDay[HVAC1] - AggDay[HVAC2] - AggDay[MiAC1] - AggDay[MiAC2] |
|11| Wtot | Water | 1 day | AggDayRest[Wtot] = AggDayDiff[Wtot] – AggDay[W1] |
|12| Mov1 | Motion | Random | AggDay[x] = SUM of movements of the day for the sensor|
