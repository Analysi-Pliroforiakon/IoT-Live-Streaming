
# Flink
#### Timestamp : 2022-10-21 00:00
#### Data : 2022-10-20 00:15, 2022-10-20 00:30… 2022-10-20 23:45, 2022-10-21 00:00(επομένης)
## Table with sensor aggs
|Index|Sensor Name|Sensor Type| Sensor Interval| Required Function|
| ---| --- | --- | --- | ---|
|1 |TH1 | Temp Sensors| 15 | AggDay[x] = AVG temperature for each sensor |
|2|TH2 | Temp Sensors| 15 | AggDay[x] = AVG temperature for each sensor |
|3 | HVAC1| HVAC | 15 | AggDay[x] = Sum wh for each sensor |
|4 | HVAC2| HVAC | 15 | AggDay[x] = Sum wh for each sensor |
|5 | MiAc1| MiAc | 15 | AggDay[x] = Sum wh for each sensor|
|6 | MiAc2| MiAc | 15 | AggDay[x] = Sum wh for each sensor|
|7| W1 | W | 15 | AggDay[x] = Sum litters of the day for sensor |
|8 | Etot | Etot | 1 day | AggDayDiff[y] = diff of value(of day y) with value(of day y-1)|
|9|Wtot |Wtot | 1 day | AggDayDiff[y] =  diff of value(of day y) with value(of day y-1) |
|10 |AggDayRest| AggDayRest | -| AggDayRest1 = AggDayDiff[Etot] - AggDay[HVAC1] - AggDay[HVAC2] - AggDay[MiAC1] - AggDay[MiAC2] |
|11| - | - | - | AggDayRest2 = AggDayDiff[Wto] – AggDay[W1] |
|?|?| Mov|  - | AggDay[x] = SUM of movements of the day for the sensor|
