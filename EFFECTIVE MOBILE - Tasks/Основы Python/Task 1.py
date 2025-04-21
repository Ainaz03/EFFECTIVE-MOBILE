class ObjList:
    def __init__(self, data):
        self.__data = data
        self.__next = None
        self.__prev = None

    # Сеттеры
    def set_next(self, obj):
        self.__next = obj

    def set_prev(self, obj):
        self.__prev = obj

    def set_data(self, data):
        self.__data = data

    # Геттеры
    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def get_data(self):
        return self.__data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
        if self.head is None:
            self.head = self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

    def remove_obj(self):
        if self.tail is None:
            return

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            prev_obj = self.tail.get_prev()
            prev_obj.set_next(None)
            self.tail = prev_obj

    def get_data(self):
        data = []
        current = self.head
        while current:
            data.append(current.get_data())
            current = current.get_next()
        return data

lst = LinkedList()
lst.add_obj(ObjList("Данные 1"))
lst.add_obj(ObjList("Данные 2"))
lst.add_obj(ObjList("Данные 3"))
res = lst.get_data()