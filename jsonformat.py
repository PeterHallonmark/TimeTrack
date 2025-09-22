

class JsonNode:
    def __init__(self, indent=2, indent_level=0):
        self._indent = indent
        self._indent_level = indent_level

    def _indent_str(self):
        return "".ljust(self._indent)

    def dump(self, data):
        return []


class JsonString(JsonNode):
    def __init__(self, name=None, indent=2, indent_level=0):
        JsonNode.__init__(self, indent, indent_level)
        self.__name = name     

    def dump(self, data):
        result = "\"" + self.__name + "\": \"{value}\""
        return result    


class JsonContainer(JsonNode):
    def __init__(self, indent=2, indent_level=2): 
        JsonNode.__init__(self, indent, indent_level)
        self._items = [] 

    def _inc_indent_level(self):
        return self._indent_level+self._indent
        
    def _start(self, name, end):
        if name:
            return "\"" + name + "\": " + end
        else:
            return end
    
    def _end(self, end):
        return end

    def _get_items(self, data):
        temp = []
        result = []
        for item in self._items:
            temp.append(item.dump(data))

        if len(temp) > 0:
            result.append(",\n".join(temp))
        else:
            # Handle no items.
            result.append("\n")    
        return result

    def add_string(self, name):
        string = JsonString(name, indent_level=self._inc_indent_level())
        self._items.append(string)
        return string

    def _add_array(self, name):
        array = JsonArray(name, indent_level=self._inc_indent_level())
        self._items.append(array)
        return array
          
    def _add_dictionary(self, name):
        dictionary = JsonDictionary(name, indent_level=self._inc_indent_level())
        self._items.append(dictionary)
        return dictionary
    
    
class JsonArray(JsonContainer):
    def __init__(self, name=None, indent=2, indent_level=0):
        JsonContainer.__init__(self, indent, indent_level)
        self.__name = name     

    def dump(self, data):
        result = [self._start(self.__name, "[")]
        temp = []
        for item in self._items:
            temp.append(item.dump(data))

        if len(temp) > 0:
            result.append(",\n".join(temp))
        else:
            # Handle no items.
            result.append("\n")
        
        result.append(self._end("]"))
        return self._indent_str() + self._indent_str().join(result)

    def add_array(self):
        return self._add_array(None)
          
    def add_dictionary(self):
        return self._add_dictionary(None)
        


class JsonDictionary(JsonContainer):
    def __init__(self, name=None, indent=2, indent_level=2):
        JsonContainer.__init__(self, indent, indent_level)
        self.__name = name
        
    def dump(self, data):
        result = [self._start(self.__name, "{")]
        
        #print(self.indent_level_str() + str(self.__name) + " " + str(len(self._items)))
        result.extend(self._get_items(data))
            
        result.append(self._end("}"))
        return "\n".join(result)

    def add_array(self, name):
        return self._add_array(name)
          
    def add_dictionary(self, name):
        return self._add_dictionary(name)
