from __future__ import annotations

from datetime import datetime


class Timer:
    def __init__(self, time_string: str) -> None:
        self.time = time_string

    def __gt__(self, _other_time: Timer) -> bool:
        return self.to_seconds() > _other_time.to_seconds()

    def __seconds_to_time(self, seconds) -> str:
        divisors = [3600, 60, 1]
        divisor_count = {}
        for divisor in divisors:
            count = seconds // divisor
            divisor_count[divisor] = count
            seconds -= (divisor * count)

        hours = str(divisor_count[3600]).rjust(2, "0")
        minutes = str(divisor_count[60]).rjust(2, "0")
        seconds = str(divisor_count[1]).rjust(2, "0")

        return f"{hours}:{minutes}:{seconds}"

    def to_seconds(self) -> int:
        time_list = self.time.split(":")
        seconds = 0
        for count, multiplier in zip(time_list, [3600, 60, 1]):
            seconds += (int(count) * multiplier)

        return seconds

    def __sub__(self, _other_time: Timer):
        self_to_seconds = self.to_seconds()
        _other_time_to_seconds = _other_time.to_seconds()

        delta = abs(self_to_seconds - _other_time_to_seconds)

        return self.__seconds_to_time(delta)

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y/%m/%d")

    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_current_datetime_with_time():
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
