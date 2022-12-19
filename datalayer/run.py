from datetime_class import DatetimeClass
from thermal_sensor import ThermalSensors
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from energy_monitors import EnergyConsomption 



def runTest(initDate):
    datetime = initDate
    print(datetime.curr_datetime)

    Sensors = ThermalSensors(datetime.curr_datetime)
    # TH1 = ThermalSensor(datetime.curr_datetime)
    # TH2 = ThermalSensor(datetime.curr_datetime, skew=-0.5)

    # air condition sensors
    energyMon = EnergyConsomption(Sensors.th1_temp, curr_datetime=datetime.curr_datetime, skew=20, random=False)
    

    hvac1_list = []
    hvac2_list = []

    temp_1_list = []
    temp_2_list = []

    miac1_list = []
    miac2_list = []

    etot_list = []

    date_list = []
    i = 0
    
    while True:
        # get temperature
        temp_1 = Sensors.th1_temp
        temp_1_list.append(temp_1)

        temp_2 = Sensors.th2_temp
        temp_2_list.append(temp_2)
        # handle air condition
        hvac1_list.append(energyMon.HVAC1)
        hvac2_list.append(energyMon.HVAC2)
        # handle miav devices
        miac1_list.append(energyMon.MiAC1)
        miac2_list.append(energyMon.MiAC2)
        # handle total energy
        
        etot_list.append(energyMon.Etot)
        # append the date
        date_list.append(datetime.curr_datetime)

        # next timestep
        datetime.step()
        # print(datetime.curr_datetime, '|', temp_1)
        Sensors.step(datetime.curr_datetime)
        energyMon.getConsumption(Sensors.th1_temp, datetime.curr_datetime)

        i += 1
        if i == 256:
            break
    # have 6 subplots
    # 3 per row
    # 2 rows
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Sensor for air condition & temperature')
    ax1.plot(date_list, temp_1_list, color='blue')
    ax1.plot(date_list, temp_2_list, color='red')
    # ax1.set_title('Temperature OutSide')
    ax1.legend(['TH1', 'TH2'])
    ax1.set_ylabel('Temperature (C)')
    ax1.set_xlabel('Date')
    
    temp_abs_list = [abs(x-20) for x in temp_1_list]
    ax2.plot(temp_abs_list, hvac1_list, color='blue')
    ax2.plot(temp_abs_list, hvac2_list, color='red')
    ax2.set_title('HVAC vs Temperature')
    ax2.legend(['HVAC1', 'HVAC2'])
    ax2.set_ylabel('HVAC (Wh)')
    ax2.set_xlabel('ABS(Temperature-20) (C)')

    ax3.plot(date_list, hvac1_list, color='blue')
    ax3.plot(date_list, hvac2_list, color='red')
    # ax3.set_title('HVAC vs Date')
    ax3.legend(['HVAC1', 'HVAC2'])
    ax3.set_ylabel('HVAC (Wh)')
    ax3.set_xlabel('Date')

    ax4.plot(date_list, miac1_list, color='blue')
    ax4.plot(date_list, miac2_list, color='red')
    # ax4.set_title('MiAC vs Date')
    ax4.legend(['MiAC1', 'MiAC2'])
    ax4.set_ylabel('MiAC (Wh)')
    ax4.set_xlabel('Date')

    # ax5 plot as step function
    ax5.step(date_list, etot_list, color='blue')
    print(etot_list)
    print(len(etot_list))
    # ax5.set_title('Total Energy vs Date')
    ax5.legend(['Total Energy'])
    ax5.set_ylabel('Total Energy (Wh)')
    ax5.set_xlabel('Date')

    # set ax6 null
    ax6.axis('off')
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