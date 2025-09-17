from datetime import datetime
import sys
import json


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


def main():
    now = datetime.now()
    print(now.strftime("%Y-%m-%d"))
    print(now.strftime("%H:%M"))
    doit()
    #currentdate = date.today()
    #print("Current Date:", current_date)
 
    return 0
    
if __name__ == "__main__":
    sys.exit(main())