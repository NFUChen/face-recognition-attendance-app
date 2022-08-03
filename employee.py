from typing import Dict, List

from timer import Timer

json = List[Dict[str, str]]


class Employee:
    def __init__(self, name: str) -> None:
        '''Create a Employee object

        Args:
            name (str): employee name
        '''
        self.name = name
        self.time_dict = {}

    def record_time(self) -> None:
        '''
        A method used to record current timestamp
        '''
        current_date = Timer.get_current_date()
        if current_date not in self.time_dict:
            self.time_dict[current_date] = {
                "on_work": None, "off_work": None
            }
        current_time = Timer.get_current_time()

        if self.time_dict[current_date]["on_work"] is None:
            self.time_dict[current_date]["on_work"] = current_time
            return

        self.time_dict[current_date]["off_work"] = current_time

    def to_json(self) -> json:
        '''
        Jsonify the stored information

        Returns:
            json (List[Dict[str, str]]): Jsonified information
        '''
        json = []
        for date in self.time_dict.keys():
            on_work_time = self.time_dict[date]["on_work"]
            off_work_time = self.time_dict[date]["off_work"]

            current_dict = {
                "name": self.name,
                "date": date,
                "on_work": on_work_time,
                "off_work": off_work_time,
                "working_hour": Timer(on_work_time) - Timer(off_work_time)
            }
            json.append(current_dict)
        return json

    def __repr__(self) -> str:
        return f"Name: {self.name}, Time Info: {self.time_dict}"
