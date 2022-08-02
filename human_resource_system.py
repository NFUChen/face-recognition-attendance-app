from typing import List, Dict
import pandas as pd
import os
from employee import Employee
from IPython.display import clear_output
from playsound import playsound

json = List[Dict[str, str]]
class HumanResourceSystem:
    def __init__(self, images_folder_path:str) -> None:
        self.images_folder_path = images_folder_path
        self.employees:Dict[str, Employee] = {}

    def _visulize_current_card_punching_status(self) -> None:
        os.system("clear")
        clear_output(wait=True)
        print(self)

    def add_employee(self, employee_name:str) -> None: 
        employee_name = employee_name.split("_")[0]

        emp = Employee(employee_name)
        self.employees[employee_name] = emp

    def is_valid_employee(self, employee_name:str) -> bool:  
        employee_name = employee_name.split("_")[0]

        return employee_name in self.employees

    def record_time_for_employee(self, employee_name:str) -> None:
        employee_name = employee_name.split("_")[0]

        if employee_name not in self.employees:
            return

        self.employees[employee_name].record_time()
        playsound('ding.mp3', block = False)
        self._visulize_current_card_punching_status()
    
    def _generate_report(self) -> json:
        report = []
        for emp in self.employees.values():
            emp_info = emp.to_json()
            report.extend(emp_info)
        return report

    def output_current_seession_punchcard_info(self) -> pd.core.frame.DataFrame:
        df = pd.DataFrame(self._generate_report())
        df["date"] = pd.to_datetime(df["date"])
        return df

    def output_csv_file(self) -> None:
        df = self.output_current_seession_punchcard_info()
        max_timestamp = str(max(df["date"]).date())
        min_timestamp = str(min(df["date"]).date())
        output_file_name = (
            min_timestamp
            if max_timestamp == min_timestamp else f"{min_timestamp}-{max_timestamp}"
        )
        df.to_csv(output_file_name,index= False)


    
        
    def __repr__(self) -> str:
        return "\n".join([repr(emp) for emp in self.employees.values()])
    
    