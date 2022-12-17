from datetime import datetime, timedelta
import time

class DatetimeClass():
    def __init__(self, wait_secs=1):
        self.curr_datetime = datetime(2020, 1, 1)
        self.wait_secs = wait_secs
    def step(self):
        self.curr_datetime += timedelta(minutes=15)
        time.sleep(self.wait_secs)
    
    

