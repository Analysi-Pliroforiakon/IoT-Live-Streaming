import random
import numpy as np
import math
import datetime
from datetime_class import DatetimeClass
import time

#changed datetime to datetime_instance for disambiguation with datetime package
datetime_instance = DatetimeClass(wait_secs=0.01)
#print(datetime_instance.curr_datetime)

def random_intervals():
    #number of times sensor is activated that day
    #can be 4 or 5 times
    motion_count = random.randrange(4, 6)
    
    intervals = []
    for i in range(motion_count):
        #generate time of the day of sensor activation
        intervals.append(random.randrange(1440))
    return sorted(intervals)

def detect_motion(curr_time):
    #print motion detection
    print(curr_time, '| 1')

def timedelta_minutes(td):
    #utility function to get minutes from timedelta format
    return (td.seconds//60)%60

def timedelta_total_seconds(td):
    return td.total_seconds()

#function to produce motion detections for next 24 hours
#generates 4-5 motion detections at random intervals

def send_motion_sigs_for_day(datetime_instance, producer=None):
    curr_time = datetime_instance.curr_datetime
    intervals = random_intervals()
    
    #list of timestamps
    daily_timestamps = []
    for intv in intervals:
        prev_time = curr_time
        #calculate datetime of next motion detection
        curr_time = datetime_instance.curr_datetime + datetime.timedelta(minutes=intv)
        daily_timestamps.append(curr_time)
        #wait according to the datetime_instance wait_secs
        #print('time to send next signal:', curr_time)
        sleep_seconds = datetime_instance.wait_secs * timedelta_total_seconds(curr_time - prev_time)/ (15*60)
        poll_start_time = time.time()
        if producer is None:
            detect_motion(curr_time)
            time.sleep(sleep_seconds)
        else:
            producer.poll(sleep_seconds)
            time.sleep(sleep_seconds-(time.time()-poll_start_time))
            producer.produce('Mov1', curr_time, 1)


#function to generate motion detections for next 24 hours
#generates 4-5 motion detections at random intervals and increments datetime_instance by 24 hours
#returns list of timestamps (optional)

def detect_for_day(datetime_instance):
    curr_time = datetime_instance.curr_datetime
    intervals = random_intervals()
    
    #list of timestamps
    daily_timestamps = []
    for intv in intervals:
        prev_time = curr_time
        #calculate datetime of next motion detection
        curr_time = datetime_instance.curr_datetime + datetime.timedelta(minutes=intv)
        daily_timestamps.append(curr_time)
        #wait according to the datetime_instance wait_secs
        #wait_secs * (number of minutes between previous and current motion detection)/15 minutes
        time.sleep(datetime_instance.wait_secs * (round(timedelta_minutes(curr_time - prev_time))/ 15))
        detect_motion(curr_time)
    #increment datetime_instance
    datetime_instance.step_day()
    #and wait appropriate amount until 24 hours after input datetime_instance
    time.sleep(datetime_instance.wait_secs * (round(timedelta_minutes(datetime_instance.curr_datetime - curr_time))/ 15))
    #optionally return timestamps
    return daily_timestamps


if __name__ == "__main__":
    total_timestamps = []
    #generate motion for 32 days
    for i in range(32):
        total_timestamps += detect_for_day(datetime_instance)
    print(len(total_timestamps))