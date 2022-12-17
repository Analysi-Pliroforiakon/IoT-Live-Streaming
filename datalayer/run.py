from datetime_class import DatetimeClass
from thermal_sensor import ThermalSensor

import matplotlib.pyplot as plt

datetime = DatetimeClass(wait_secs=0.01)
print(datetime.curr_datetime)

TH1 = ThermalSensor(datetime.curr_datetime)
TH2 = ThermalSensor(datetime.curr_datetime, skew=-0.5)
temp_1_list = []
temp_2_list = []
i = 0
while True:
    # get temperature
    temp_1 = TH1.curr_temp
    temp_1_list.append(temp_1)

    temp_2 = TH2.curr_temp
    temp_2_list.append(temp_2)

    # next timestep
    datetime.step()
    print(datetime.curr_datetime, '|', temp_1)
    TH1.step(datetime.curr_datetime)
    TH2.step(datetime.curr_datetime)
    i += 1
    if i == 256:
        break
plt.plot(temp_1_list)
plt.plot(temp_2_list)
plt.show()
