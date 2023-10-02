class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None

class Stack:
    def __init__(self):
        self.head = None

    def push(self, value):
        node = Node(value)
        node.prev = self.head
        self.head = node

    def pop(self):
        node = self.head
        value = node.value if node is not None else None
        self.head = node.prev if node is not None else None
        del node
        return value
    
    def is_empty(self):
        return self.head is None