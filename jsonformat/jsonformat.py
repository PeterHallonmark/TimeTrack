

class JSONNode:
    def __init__(self, name, indent=2):
        self.name = name
        self._indent = indent

    def dump(self, data):
        builder = JSONBuilder()
        self.accept(builder)
        return builder.get_result()
        
    def accept(self, visitor):
        visitor.visit_node(self)


class JSONString(JSONNode):
    def __init__(self, name=None, indent=2):
        JSONNode.__init__(self, name, indent)
        self.__name = name


class JSONContainer(JSONNode):
    def __init__(self, name=None, indent=2):
        JSONNode.__init__(self, name, indent)
        self._items = []

    def accept_items(self, visitor):
        for item in self._items:
            item.accept(visitor)

    def add_string(self, name):
        string = JSONString(name)
        self._items.append(string)
        return string

    def _add_array(self, name):
        array = JSONArray(name)
        self._items.append(array)
        return array

    def _add_dictionary(self, name):
        dictionary = JSONDictionary(name)
        self._items.append(dictionary)
        return dictionary


class JSONArray(JSONContainer):
    def __init__(self, name=None, indent=2):
        JSONContainer.__init__(self, name, indent)

    def add_array(self):
        return self._add_array(None)

    def add_dictionary(self):
        return self._add_dictionary(None)

    def accept(self, visitor):
        visitor.visit_array(self)


class JSONDictionary(JSONContainer):
    def __init__(self, name=None, indent=2):
        JSONContainer.__init__(self, name, indent)

    def accept(self, visitor):
        visitor.visit_dictionary(self)

    def add_array(self, name):
        return self._add_array(name)

    def add_dictionary(self, name):
        return self._add_dictionary(name)


class IndentationLevel:
    def __init__(self):
        self.__level = 0

    def inc(self, level=2):
        self.__level += level

    def dec(self, level=2):
        self.__level -= level

    def __str__(self):
        return "".ljust(self.__level)


class JSONBuilder:
    def __init__(self):
        self.__result = []
        self.__indentation = IndentationLevel()

    def visit_dictionary(self, dictionary):
        if dictionary.name is not None:
            self.__result.append(f"{self.__indentation}{dictionary.name}: {{")
        else:
            self.__result.append(f"{self.__indentation}{{")
        self.__indentation.inc()
        dictionary.accept_items(self)
        self.__indentation.dec()
        self.__result.append(f"{self.__indentation}}}")

    def visit_array(self, array):
        if array.name is not None:
            self.__result.append(f"{self.__indentation}{array.name}: [")
        else:
            self.__result.append(f"{self.__indentation}[")
        self.__indentation.inc()
        array.accept_items(self)
        self.__indentation.dec()
        self.__result.append(f"{self.__indentation}]")

    def get_result(self):
        return "\n".join(self.__result)

    def visit_node(self, node):
        self.__result.append(f"{self.__indentation}{node.name}")