class ObjList:
    def  __init__(self,data) -> None:
        self.__data=data
        self.__next=self.__prev=None

    def set_next(self, obj) :
         self.__next=obj


    def set_prev(self, obj) :
        self.__prev=obj


    def get_next(self) :
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_data(self, data) :
        self.__data=data


    def get_data(self) :
        return self.__data

class LinktList:
    def __init__(self) -> None:
        self.head=None
        self.tail=None

    def add_obj(self,obj):
        if self.tail:
            self.tail.set_next(obj)
        obj.set_prev(self.tail)
        self.tail=obj
        if not self.head:
            self.head=obj


    def remove_obj(self):
        if self.tail is None:
            return
        prev=self.tail.get_prev()
        if prev:
            prev.set_next(None)

        self.tail=prev
        if self.tail is None:
            self.head=None     



    def get_data(self) :
        s=[]
        h=self.head
        while h:
            s.append(h.get_data())
            h=h.get_next()
        return s




