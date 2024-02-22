from my_math.Linked_list import LinkedList


class LinkedList_vectors(LinkedList):
    def __init__(self):
        super().__init__()
        self.l_set = set()

    def add_to_end(self, value):
        super().add_to_end(value)
        self.l_set.add(value.x * 1000 + value.y)

    def add_to_beginning(self, value):
        super().add_to_beginning(value)
        self.l_set.add(value.x * 1000 + value.y)

    def delete_end(self):
        a = self.tail.next.value
        super().delete_end()
        self.l_set.remove(a.x * 1000 + a.y)

    def delete_first(self):
        a = self.head.previous.value
        super().delete_first()
        self.l_set.remove(a.x * 1000 + a.y)

    def __contains__(self, item):
        return (item.x * 1000 + item.y) in self.l_set
