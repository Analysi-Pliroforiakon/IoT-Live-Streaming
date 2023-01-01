from datetime import datetime, timedelta
import time

class DatetimeClass():
    def __init__(self, wait_secs=1):
        self.curr_datetime = datetime(2020, 1, 1)
        self.wait_secs = wait_secs
    def step(self, skip_secs=0):
        self.curr_datetime += timedelta(minutes=15)
        time.sleep(max(self.wait_secs-skip_secs, 0))
    #increment datetime by 1 day
    def step_day(self):
        self.curr_datetime += timedelta(days=1)
        time.sleep(self.wait_secs)
    def setFromDatetime(self, another_datetime):
        self.curr_datetime = another_datetime
    
    

