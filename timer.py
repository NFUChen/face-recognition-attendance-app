from __future__ import annotations
from datetime import datetime
class Timer:
    def __init__(self, time_string:str) -> None:
        self.time = time_string
    
    def __gt__(self, _other_time:Timer) -> bool:
        return self.to_seconds() > _other_time.to_seconds()
     

    def to_seconds(self) -> int:
        time_list = self.time.split(":")
        seconds = 0 
        for count, multiplier in zip(time_list, [3600, 60, 1]):
            seconds += (int(count) * multiplier)
        
        return seconds

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y/%m/%d")
    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_current_datetime_with_time():
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")