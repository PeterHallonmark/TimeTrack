

class JSONNode:
    def __init__(self, indent=2):
        self._indent = indent

    def _indent_str(self):
        return "".ljust(self._indent)

    def dump(self, data):
        builder = JSONBuilder()
        self.accept(builder)
        return builder.get_result()
        
    def accept(self, visitor):
        visitor.visit_node(self)


class JSONString(JSONNode):
    def __init__(self, name=None, indent=2):
        JSONNode.__init__(self, indent)
        self.__name = name


class JSONContainer(JSONNode):
    def __init__(self, indent=2):
        JSONNode.__init__(self, indent)
        self._items = []

    def _inc_indent_level(self):
        return self._indent

    def _start(self, name, end):
        if name:
            return "\"" + name + "\": " + end
        else:
            return end

    def _end(self, end):
        return end

    def accept_items(self, visitor):
        for item in self._items:
            item.accept(visitor)

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
        JSONContainer.__init__(self, indent)
        self.name = name

    def add_array(self):
        return self._add_array(None)

    def add_dictionary(self):
        return self._add_dictionary(None)

    def accept(self, visitor):
        visitor.visit_array_start(self)
        self.accept_items(visitor)
        visitor.visit_array_end(self)


class JSONDictionary(JSONContainer):
    def __init__(self, name=None, indent=2):
        JSONContainer.__init__(self, indent)
        self.name = name

    def accept(self, visitor):
        visitor.visit_dictionary_start(self)
        self.accept_items(visitor)
        visitor.visit_dictionary_end(self)

    def add_array(self, name):
        return self._add_array(name)

    def add_dictionary(self, name):
        return self._add_dictionary(name)


class JSONBuilder:
    def __init__(self):
        self.__result = []

    def visit_dictionary_start(self, dictionary):
        if dictionary.name is not None:
            self.__result.append(f"{dictionary.name}: {{")
        else:
            self.__result.append(f"{{")

    def visit_dictionary_end(self, dictionary):
        self.__result.append("}")

    def visit_array_start(self, array):
        if array.name is not None:
            self.__result.append(f"{array.name}: [")
        else:
            self.__result.append(f"[")

    def visit_array_end(self, array):
        self.__result.append(f"]")

    def get_result(self):
        return "\n".join(self.__result)

    def visit_node(self, node):
        self.__result.append("<node>")