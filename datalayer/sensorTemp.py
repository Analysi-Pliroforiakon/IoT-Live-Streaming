import calendar
import datetime
import random
from generateTemp import get_random_temperature


def generate_temperature_data(timestamp):
    # Get a random temperature for the given timestamp
    temperature = get_random_temperature(timestamp)

    # Generate a random error value within a range of +/- 0.5 degrees Celsius
    error = random.uniform(-0.5, 0.5)

    # Add the error value to the temperature to simulate a sensor reading
    sensor_reading = temperature + error

    # Return the sensor reading and the timestamp as a tuple
    return (sensor_reading, timestamp)
