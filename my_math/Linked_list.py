class node:
    def __init__(self, value=None, next=None, previous=None):
        self.value = value
        self.next: node = next
        self.previous: node = previous


class LinkedList:
    def __init__(self):
        self.head = node()
        self.tail = node()
        self.head.previous = self.tail
        self.tail.next = self.head
        self.length = 0

    def __len__(self):
        return self.length

    def add_to_beginning(self, value):
        # print(self.length)
        new = node(value)

        self.head.previous.next = new
        new.next = self.head
        new.previous = self.head.previous
        self.head.previous = new

        self.length += 1

    def add_to_end(self, value):
        new = node(value)

        self.tail.next.previous = new
        new.next = self.tail.next
        self.tail.next = new
        new.previous = self.tail

        self.length += 1

    def delete_end(self):
        old = self.tail.next
        self.tail.next = self.tail.next.next
        self.tail.next.previous = self.tail
        old.next = None
        old.previous = None

        self.length -= 1

    def delete_first(self):
        old = self.head.previous
        self.head.previous = self.head.previous.previous
        self.head.previous.next = self.head
        old.next = None
        old.previous = None

        self.length -= 1

    def __getitem__(self, item):
        # print(item, self.length)
        if item >= self.length:
            raise IndexError

        if item == -1 and self.length:
            return self.tail.next.value

        start = self.head.previous
        for _ in range(item):
            start = start.previous
        return start.value

    def __str__(self):
        n = self.head.previous
        result = ""
        for _ in range(self.length):
            result += str(n.value) + "<->"
            n = n.previous
        return result[:-3]


# l = LinkedList()
# l.add_to_beginning(3)
# l.add_to_beginning(4)
# l.add_to_end(2)
#
# print(l)
# print(l[3])
