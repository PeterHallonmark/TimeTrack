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
                return json.load(file)
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

    
class JsonTree2:
    def _init__(self, indent=2):
        self.__indent = indent
        self.__indent_level = 0
        self.__keywords = { 
                "timetrack": self.section
            }

    def _inc(self, text):
        result = "".ljust(self.__indent_level) + text
        self.__indent_level += self.__indent
        return result
        
    def _dec(self, text):
        self.__indent_level -= self.__indent      
        return "".ljust(self.__indent_level) + text
        
    def out(self, data):
        result = []
        #for item in data:
            #result.extend(self.__keywords[item](item, data[item]))
        print("\n".join(result)) 

    def section(self, name, data):
        result = [self.__inc("\"" + name + "\": {")]
        if type(data) == list:
            result.extend(self.array(data))
        result.append(self.__dec("}"))
        return result

    def array(self, data):
        result = [self.__inc("[")]
        print(data)
        result.append(self.__dec("]"))
        return result


        
class JsonBuilder:
    def __init__(self):
        pass
        
    def add_array(self):
        pass
        
    def add_dict(self):
        pass
        

class JsonNode:
    def __init__(self, indent=2, indent_level=0):
        self._indent = indent
        self._indent_level = indent_level

    def indent_level_str(self):
        return "".ljust(self._indent_level)

    def dump(self, data):
        return []


class JsonString(JsonNode):
    def __init__(self, name=None, indent=2, indent_level=0):
        JsonNode.__init__(self, indent, indent_level)
        self.__name = name     

    def dump(self, data):
        result = [self.indent_level_str() + self.__name + "\": \"{value}\""]
        return result    


class JsonContainer(JsonNode):
    def __init__(self, indent=2, indent_level=2): 
        JsonNode.__init__(self, indent, indent_level)
        self._items = [] 

    def _inc_indent_level(self):
        return self._indent_level+self._indent
        
    def _start(self, name, end):
        if name:
            return self.indent_level_str() + "\"" + name + "\": " + end
        else:
            return self.indent_level_str() + end
    
    def _end(self, end):
        return "".ljust(self._indent_level) + end

    def add_string(self, name):
        string = JsonString(name, indent_level=self._inc_indent_level())
        self._items.append(string)
        return string

    def add_array(self, name):
        array = JsonArray(name, indent_level=self._inc_indent_level())
        self._items.append(array)
        return array
          
    def add_dictionary(self, name):
        dictionary = JsonDictionary(name, indent_level=self._inc_indent_level())
        self._items.append(dictionary)
        return dictionary
    
    
class JsonArray(JsonContainer):
    def __init__(self, name=None, indent=2, indent_level=0):
        JsonContainer.__init__(self, indent, indent_level)
        self.__name = name     

    def dump(self, data):
        result = [self._start(self.__name, "[")]
        
        for item in self._items:
            result.extend(item.dump(data))

        result.append(self._end("]"))
        return result
    

class JsonDictionary(JsonContainer):
    def __init__(self, name=None, indent=2, indent_level=2):
        JsonContainer.__init__(self, indent, indent_level)
        self.__name = name
        
    def dump(self, data):
        result = [self._start(self.__name, "{")]
        
        for item in self._items:
            result.extend(item.dump(data))

        result.append(self._end("}"))
        return result
        


def main():
    #json = JsonTree()
    
    #with open('data.json', 'r') as file:
    #    data = json.load(file)
    data = []
    xx = JsonDictionary(indent=4)
    xx.add_array("activities")
    period = xx.add_dictionary("period")
    period.add_string("name")
    period.add_string("start")
    period.add_string("end")
    
    xx.add_array("weeks")
    
    print("\n".join(xx.dump(data)))
    #tr = TimeRegister("data.json")
    #tr.start_activity()
    #tr.store()
    
    data = {
        "timetrack": [
            {"start": "09.50", "end": "11.00", "activity": "intro"},
            {"start": "11.00", "end": "12.00", "away": "lunch"},
            {"start": "12.00", "end": "16.00", "activity": "intro"},
        ]
    }
    
    
    
    
    #x = JsonTree()
    #x.out(data)

    
    #currentdate = date.today()
    #print("Current Date:", current_date)
 
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
