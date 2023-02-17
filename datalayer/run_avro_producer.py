from water_sensor import TotalWaterSensor, WaterSensor
from datetime_class import DatetimeClass
from thermal_sensor import ThermalSensors
from energy_monitors import EnergyConsumption 
from motion_sensor import send_motion_sigs_for_day
from producer_class import AvroProducerClass
import datetime
import threading
import time
import argparse

parser = argparse.ArgumentParser(
    description="Kafka Producer for Sensor Data",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

optional = parser._action_groups.pop()
optional.add_argument('-w', '--wait-secs', type=float, default=1,
                help='Seconds that correspond to real quarters of an hour')
optional.add_argument('-q', '--quarter-limit', type=int, default=None,
                help='Limit the number of quarters of an hour for which the script is running')
parser._action_groups.append(optional)
args = parser.parse_args()

producer = AvroProducerClass()
dt = DatetimeClass(wait_secs=args.wait_secs)

print(dt.curr_datetime)

th_sensors = ThermalSensors(dt.curr_datetime)

# air condition sensors
energyMon = EnergyConsumption(th_sensors.th1_temp, curr_datetime=dt.curr_datetime, skew=20, random=False)

# water sensors
W1 = WaterSensor(dt.curr_datetime)
Wtot = TotalWaterSensor(dt.curr_datetime)
time.sleep(2)

i = 0
thread = threading.Thread(target=send_motion_sigs_for_day, args=[dt, producer])
thread.start()
while True:
    # handle temperature
    producer.produce('TH1', dt.curr_datetime, th_sensors.th1_temp)
    producer.produce('TH2', dt.curr_datetime, th_sensors.th2_temp)

    # handle air condition
    producer.produce('HVAC1', dt.curr_datetime, energyMon.HVAC1)
    producer.produce('HVAC2', dt.curr_datetime, energyMon.HVAC2)

    # handle miav devices
    producer.produce('MiAC1', dt.curr_datetime, energyMon.MiAC1)
    producer.produce('MiAC2', dt.curr_datetime, energyMon.MiAC2)

    # handle total energy
    if dt.curr_datetime.hour == 0 and dt.curr_datetime.minute == 0:
        producer.produce('Etot', dt.curr_datetime, energyMon.Etot)
        producer.produce('Wtot', dt.curr_datetime, Wtot.get_measurement())

    # handle water consumption
    water_1 = W1.get_measurement()
    producer.produce('W1', dt.curr_datetime, water_1['current_consumption'])
    if water_1['2 days back'] is not None:
        late_datetime = dt.curr_datetime - datetime.timedelta(days=2)
        producer.produce('W1', late_datetime, water_1['2 days back'])
    if water_1['10 days back'] is not None:
        very_late_datetime = dt.curr_datetime - datetime.timedelta(days=10)
        producer.produce('W1', very_late_datetime, water_1['10 days back'])

    # next timestep
    poll_start_time = time.time()
    #link about polling: https://github.com/confluentinc/confluent-kafka-python/issues/137
    producer.flush(dt.wait_secs*0.9)
    #producer.poll(0)
    secs_passed = time.time() - poll_start_time
    dt.step(skip_secs=secs_passed)
    th_sensors.step(dt.curr_datetime)
    energyMon.getConsumption(th_sensors.th1_temp, dt.curr_datetime)

    W1.step(dt.curr_datetime)

    if dt.curr_datetime.hour == 0 and dt.curr_datetime.minute == 0:
        Wtot.step(dt.curr_datetime)
        thread = threading.Thread(target=send_motion_sigs_for_day, args=[dt, producer])
        thread.start()

    i += 1
    if i == args.quarter_limit:
        break

producer.flush()
print('Main script ended. Press Ctrl+C to kill thread..')

