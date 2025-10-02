#!/usr/bin/python3

from datetime import datetime
import sys
import json
import jsonformat

def doit():
    data = []
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except:
        pass

    now = datetime.now()
    
    # Append new data
    new_data = {"date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M")
                }
    data.append(new_data)  # Assuming the JSON file contains a list

    # Write the updated data back to the file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty formatting


#class 
#    def date(self):
#        return date.strftime("%Y-%m-%d")
#
#    def time(self):
#        return date.strftime("%H:%M")
#
#    def week(self):
#        return date.isocalendar().week



class TimeRegister:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__read_json(filename)
        self.__activities = self.__read_activities()

    def __read_json(self, filename):
        try:
            with open(filename, 'r') as file:
                return JSON.load(file)
        except:
            return []

    def __read_activities(self):
        try:
            print(self.__data["activities"])
        except:
            return {}

    def start_activity(self, date=datetime.now()):
        now = date

        #print(self.__week(date))
        #new_data = {"date": now.strftime("%Y-%m-%d"),
        #            "time": now.strftime("%H:%M")
        #           }
        #self.__data.append(new_data)
        
    def end_activity(self, activity, date=datetime.now()):
        pass
        
    def change_activity(self, activity, date=datetime.now()):
        pass
               
    def store(self):
        with open(self.__filename, 'w') as file:
            json.dump(self.__data, file, indent=4)


def main():
    #JSON = JSONTree()
    
    #with open('data.JSON', 'r') as file:
    #    data = JSON.load(file)
    data = []
    xx = jsonformat.JSONDictionary(indent=2)
    xx.add_array("activities")
    period = xx.add_array("period")
    period.add_string("name")
    period.add_string("start")
    period.add_string("end")
    
    weeks = xx.add_array("weeks")
    week = weeks.add_dictionary()
    week.add_string("week")
    
    timetrack = week.add_array("timetrack")
    x = timetrack.add_dictionary()
    x.add_string("start")
    x.add_string("end")
    x.add_string("activity")
    
    print(xx.dump(None))
    #tr = TimeRegister("data.JSON")
    #tr.start_activity()
    #tr.store()
    
    data = {
        "timetrack": [
            {"start": "09.50", "end": "11.00", "activity": "intro"},
            {"start": "11.00", "end": "12.00", "away": "lunch"},
            {"start": "12.00", "end": "16.00", "activity": "intro"},
        ]
    }
    
    
    
    
    #x = JSONTree()
    #x.out(data)

    
    #currentdate = date.today()
    #print("Current Date:", current_date)
 
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
