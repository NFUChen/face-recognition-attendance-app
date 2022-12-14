import os
from typing import Dict, List

import pandas as pd
from IPython.display import clear_output
from playsound import playsound

from .employee import Employee

json = List[Dict[str, str]]


class HumanResourceSystem:
    def __init__(self) -> None:
        '''Create a HumanResourceSystem to track emplayee attendance
        '''
        self.employees: Dict[str, Employee] = {}

    def _visulize_current_card_punching_status(self) -> None:
        os.system("clear")
        clear_output(wait=True)
        print(self)
        
    def __repr__(self) -> str:
        return "\n".join([repr(emp) for emp in self.employees.values()])

    def add_employee(self, employee_name: str) -> None:
        '''
        Args:
            employee_name (str): employee name wants to add into the system
        '''
        employee_name = employee_name.split("_")[0]

        emp = Employee(employee_name)
        self.employees[employee_name] = emp

    def is_valid_employee(self, employee_name: str) -> bool:
        '''
        Check wheter a given employee name is in the system or not

        Args:
            employee_name (str): employee to check whether he/she is within the system

        Returns:
            bool: True indicating that the given employee is added into the system
        '''
        employee_name = employee_name.split("_")[0]

        return employee_name in self.employees

    def record_time_for_employee(self, employee_name: str) -> None:
        '''
        A method used to record the timestamp for a employee

        Args:
            employee_name (str): employee name wants to record
        '''
        employee_name = employee_name.split("_")[0]

        if employee_name not in self.employees:
            return

        self.employees[employee_name].record_time()
        playsound('./face_recognizer/ding.mp3', block=False)
        self._visulize_current_card_punching_status()

    def _generate_report(self) -> json:
        report = []
        for emp in self.employees.values():
            emp_info = emp.to_json()
            report.extend(emp_info)
        return report

    def output_current_seession_punchcard_info(self) -> pd.core.frame.DataFrame:
        '''
        Output timestamp information collected as a DataFrame

        Returns:
            pd.core.frame.DataFrame: DataFrame containing timestamp collected
        '''
        df = pd.DataFrame(self._generate_report())
        df["date"] = pd.to_datetime(df["date"])
        return df

    def output_csv_file(self) -> None:
        '''
        Output timestamp information collected from .output_current_seession_punchcard_info method to a csv file
        '''
        df = self.output_current_seession_punchcard_info()
        max_timestamp = str(max(df["date"]).date()).replace("-", "")
        min_timestamp = str(min(df["date"]).date()).replace("-", "")
        output_file_name = (
            min_timestamp
            if max_timestamp == min_timestamp else f"{min_timestamp}-{max_timestamp}"
        )
        df.to_csv(output_file_name, index=False)

    
