class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class OneLinkedList:

    def __init__(self):
        self.head = self.tail = None

    def push_back(self, data):
        node = Node(data)
        if self.head is None:
            self.head = self.tail = node
            return None
        self.tail.next = node
        self.tail = node
        return None

    def push_front(self, data):
        node = Node(data)
        if self.head is None:
            self.head = self.tail = node
            return None
        node.next = self.head
        self.head = node
        return None

    def pop_front(self):
        if self.head is None:
            return None
        if self.head == self.tail:
            self.head = self.tail = None
            return None
        self.head = self.head.next
        return None

    def pop_back(self):
        if self.head is None:
            return None
        if self.head == self.tail:
            self.head = self.tail = None
            return None
        node = self.head
        while node.next != self.tail:
            node = node.next
        node.next = None
        self.tail = node
        return None

    def get_attr(self, index):
        if self.head is None:
            return None
        if self.head == self.tail:
            return self.head.data
        node = self.head
        it = 0
        while it != index and node != self.tail:
            node = node.next
            it += 1
        return node.data

    def insert(self, index, data):
        if index < 1:
            self.push_front(data)
            return None
        if self.head == self.tail:
            self.push_back(data)
            return None
        left = self.head
        it = 1
        while it != index and left.next is not None:
            left = left.next
            it += 1
        if left == self.tail:
            self.push_back(data)
            return None
        node = Node(data)
        node.next = left.next
        left.next = node
        return None

    def erase(self, index):
        if self.head is None:
            return None
        if self.head == self.tail:
            self.pop_back()
            return None
        if index <= 0:
            self.pop_front()
            return None
        left = self.head
        it = 1
        while it != index and left != self.tail:
            left = left.next
            it += 1
        if left.next is None or left.next == self.tail:
            self.pop_back()
            return None
        node = left.next
        left.next = node.next
        return None

