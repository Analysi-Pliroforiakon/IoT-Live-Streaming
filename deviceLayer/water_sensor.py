import numpy as np
import random

def bell(x, mean, std):
        y_out = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
        return y_out

# run this script to overview the avg consumption curve
def avg_consumption(time_of_day):
    return (bell(time_of_day, 7, 2.1) + bell(time_of_day, 23, 2.5) + bell(time_of_day, 16, 5))*3 + 0.18

class WaterSensor():
    def __init__(self, curr_datetime):
        # All member variables are modified by self.step()
        self.curr_consumption = None
        # Initialize history with dummy values for the first late events
        self.consumption_hist = [random.uniform(0, 1) for _ in range(10*24*15)]
        self.step_count = 0
        self.step(curr_datetime)

    def get_measurement(self):
        if (self.step_count -1) % 20 == 0:
            # Get a 2 days old measurement
            late_event = self.consumption_hist[-(2*24*15)]
        else:
            late_event = None
        
        if (self.step_count-1 )% 120 == 0:
            # Gat a 10 days old measurement
            very_late_event = self.consumption_hist[-(10*24*15)]
        else:
            very_late_event = None

        return {
            'current_consumption': self.curr_consumption,
            '2 days back': late_event,
            '10 days back': very_late_event
        }

    def step(self, curr_datetime):
        if curr_datetime.minute == 0:
            self.daily_mean = random.uniform(-0.1, 0.1)
        # Get time of day in decimal hour form. e.g. 13.5 is equivalent to 13:30
        decimal_hour = curr_datetime.hour + curr_datetime.minute/60
        self.curr_consumption = avg_consumption(decimal_hour) \
                                + self.daily_mean \
                                + random.uniform(-0.1, 0.1)
        self.consumption_hist.append(self.curr_consumption)

        # Keep data of last 10 days
        self.consumption_hist = self.consumption_hist[-(10*24*15):]

        self.step_count += 1

class TotalWaterSensor():
    def __init__(self, curr_datetime=None):
        self.current_total = 1000
    
    def get_measurement(self):
        return self.current_total
    
    def step(self, curr_datetime):
        assert curr_datetime.hour == 0 and curr_datetime.minute == 0, \
            'step() was not called at the start of the day'

        self.current_total += 110 + random.uniform(-10, 10)



# present info about simulated consumption
if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt
    import scipy.integrate as integrate
    from datetime_class import DatetimeClass

    datetime = DatetimeClass(wait_secs=0.01)

    W1 = WaterSensor(datetime.curr_datetime)
    Wtot = TotalWaterSensor(datetime.curr_datetime)
    w_1_list = []
    wtot_list = []
    i = 0
    while True:
        # get current water consumption measurements
        water_1 = W1.get_measurement()
        w_1_list.append(water_1['current_consumption'])

        wtot = Wtot.get_measurement()
        wtot_list.append(wtot)
        print(datetime.curr_datetime, '|', water_1, '|', wtot)

        # next timestep
        datetime.step()
        W1.step(datetime.curr_datetime)

        # advance daily sensors
        if datetime.curr_datetime.hour == 0 and datetime.curr_datetime.minute == 0:
            Wtot.step(datetime.curr_datetime)

        i += 1
        if i == 256:
            break

    plt.plot(w_1_list)
    plt.title('W1 measurements')
    plt.show()

    print(f"avg total daily consumption: {integrate.quad(avg_consumption, 0, 24)[0]:.4f}")

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    x = np.linspace(0, 24, 100)

    plt.plot(x, avg_consumption(x), color='red')
    plt.title('Average water consumption per day (in lt)')
    plt.show()

    plt.plot(wtot_list)
    plt.title('Wtot measurements')
    plt.show()
