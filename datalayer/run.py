from datetime_class import DatetimeClass
from thermal_sensor import ThermalSensors
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from air_condition_energy_monitor import AirConditionEnergyConsomption 



def runTest(initDate):
    datetime = initDate
    print(datetime.curr_datetime)

    Sensors = ThermalSensors(datetime.curr_datetime)
    # TH1 = ThermalSensor(datetime.curr_datetime)
    # TH2 = ThermalSensor(datetime.curr_datetime, skew=-0.5)

    # air condition sensors
    AirCondition = AirConditionEnergyConsomption(Sensors.th1_temp, skew=20, random=False)
    

    hvac1_list = []
    hvac2_list = []

    temp_1_list = []
    temp_2_list = []
    date_list = []
    i = 0
    
    while True:
        # get temperature
        temp_1 = Sensors.th1_temp
        temp_1_list.append(temp_1)

        temp_2 = Sensors.th2_temp
        temp_2_list.append(temp_2)
        # handle air condition
        hvac1_list.append(AirCondition.HVAC1)
        hvac2_list.append(AirCondition.HVAC2)

        # append the date
        date_list.append(datetime.curr_datetime)

        # next timestep
        datetime.step()
        # print(datetime.curr_datetime, '|', temp_1)
        Sensors.step(datetime.curr_datetime)
        AirCondition.getConsumption(Sensors.th1_temp)

        i += 1
        if i == 256:
            break
    plt.title('Temperature OutSide')
    plt.plot( date_list, temp_1_list, color='blue')
    plt.plot( date_list, temp_2_list, color='red')
    plt.show()

    plt.title('HVAC1 and HVAC2')
    plt.plot( temp_1_list, hvac1_list, color='blue')
    plt.plot( temp_1_list, hvac2_list, color='red')
    plt.show()
# dummyDate = DatetimeClass(wait_secs=0.01)
# # run test for 2020-01-01 
# runTest(dummyDate)

dummyDate2 = DatetimeClass(wait_secs=0.01)
# print(dummyDate2)
# dummyDate2.setFromDatetime(datetime(2020, 7, 1))
# print(dummyDate2.curr_datetime)
# run test for 2020-07-01
runTest(dummyDate2)