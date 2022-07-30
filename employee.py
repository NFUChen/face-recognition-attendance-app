from timer import Timer
class Employee:
    def __init__(self, chi_name:str) -> None:
        self.chi_name = chi_name
        self.time_dict = {}
        
    def get_chinese_name(self) -> str:
        return self.chi_name
    
    def record_time(self) -> str:
        current_date = Timer.get_current_date()
        if current_date not in self.time_dict:
            self.time_dict[current_date] = {
                "on_work":None, "off_work":None
            }
        current_time = Timer.get_current_time()
        
        if self.time_dict[current_date]["on_work"] is None:
            self.time_dict[current_date]["on_work"] = current_time
            return

                
        self.time_dict[current_date]["off_work"] = current_time

    def __repr__(self) -> str:
        return f"Name: {self.chi_name}, Time Info: {self.time_dict}"


        
    