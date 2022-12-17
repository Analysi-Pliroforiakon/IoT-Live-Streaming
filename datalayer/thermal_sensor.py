import random
import numpy as np
import math
import datetime

def get_random_temperature(dt):
    # Convert the timestamp to a datetime object
    #dt = datetime.datetime.fromtimestamp(timestamp)

    # Get the month and year from the datetime object
    month = dt.month
    year = dt.year

    # Average temperatures in Athens, Greece by month (in Celsius)
    temperatures = [12.5, 13.5, 16.0, 19.0, 24.0,
                    28.0, 30.5, 30.0, 26.0, 21.0, 16.0, 13.0]

    # Get the average temperature for the corresponding month
    avg_temp = temperatures[month - 1]

    # Generate a random temperature within a range of +/- 3 degrees Celsius around the average temperature
    random_temp = avg_temp + random.uniform(-1, 1)

    return random_temp

class ThermalSensor():
    def __init__(self, curr_datetime, skew=0):
        self.peak_temp = self.get_new_peak(curr_datetime)
        self.low_temp = self.get_new_low(curr_datetime)
        mean = (self.peak_temp-self.low_temp)/2
        self.temp_points = (np.sin(np.linspace(math.pi/2, 3*math.pi/2, 14*4))+1)*mean + self.low_temp
        self.curr_pos = 8*4 - 1
        self.skew = skew
        self.curr_temp = self.temp_points[self.curr_pos] + random.uniform(-0.5+self.skew, 0.5+self.skew)

    def step(self, curr_datetime):
        #TODO: find pos from hour and minutes
        #hour = curr_datetime.hour
        #minutes = curr_datetime.minutes
        #if hour

        if curr_datetime.hour==16 and curr_datetime.minute==0:
            self.low_temp = self.get_new_low(curr_datetime)
            mean = (self.peak_temp-self.low_temp)/2
            self.temp_points = (np.sin(np.linspace(math.pi/2, 3*math.pi/2, 14*4))+1)*mean + self.low_temp
            self.curr_pos = 0
        elif curr_datetime.hour==6 and curr_datetime.minute==0:
            self.peak_temp = self.get_new_peak(curr_datetime)
            mean = (self.peak_temp-self.low_temp)/2
            self.temp_points = (np.sin(np.linspace(-math.pi/2, math.pi/2, 10*4))+1)*mean + self.low_temp
            self.curr_pos = 0
        else:
            self.curr_pos += 1

        self.curr_temp = self.temp_points[self.curr_pos] + random.uniform(-0.5+self.skew, 0.5+self.skew)
    
    def get_new_peak(self, curr_datetime):
        mean_temp = get_random_temperature(curr_datetime)
        peak_temp = mean_temp + random.uniform(2, 7)
        return peak_temp

    def get_new_low(self, curr_datetime):
        mean_temp = get_random_temperature(curr_datetime)
        low_temp = mean_temp - random.uniform(7, 2)
        return low_temp