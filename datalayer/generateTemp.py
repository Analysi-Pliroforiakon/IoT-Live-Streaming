import calendar
import datetime
import random


def get_random_temperature(timestamp):
    # Convert the timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(timestamp)

    # Get the month and year from the datetime object
    month = dt.month
    year = dt.year

    # Average temperatures in Athens, Greece by month (in Celsius)
    temperatures = [12.5, 13.5, 16.0, 19.0, 24.0,
                    28.0, 30.5, 30.0, 26.0, 21.0, 16.0, 13.0]

    # Get the average temperature for the corresponding month
    avg_temp = temperatures[month - 1]

    # Generate a random temperature within a range of +/- 3 degrees Celsius around the average temperature
    random_temp = avg_temp + random.uniform(-3, 3)

    return random_temp
