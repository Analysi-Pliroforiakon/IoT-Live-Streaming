

|Sensor Type| Sensor Interval| Required Function|
| --- | --- | ---|
| Temp Sensors| 15 | AggDay[x] = AVG temperature for each sensor |
| HVAC | 15 | AggDay[x] = Sum wh for each sensor |
| MiAc | 15 | AggDay[x] = Sum wh for each sensor|
| Etot | 1 day | AggDayDiff[y] = diff of max(of day y) with max(of day y-1)|
| Mov|  - | AggDay[x] = SUM of movements of the day for the sensor|
| W1 | 15 | AggDay[x] = Sum litters of the day for sensor |
|Wtot | 1 day | AggDayDiff[y] =  diff of max(of day y) with max(of day y-1) |
| - | -| AggDayRest1 = AggDayDiff[Etot] - AggDay[HVAC1] - AggDay[HVAC2] - AggDay[MiAC1] - AggDay[MiAC2] |
| - | - | AggDayRest2 = AggDayDiff[Wto] – AggDay[W1] |