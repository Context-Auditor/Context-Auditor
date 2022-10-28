class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []


    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        if( not self.isEmpty()):
            return self.items.pop(0)
        else:
            return False

    def peek(self):
        if (not self.isEmpty()):
            return self.items[0]
        else:
            return 'any'

    def size(self):
        return len(self.items)

    def empty(self):
        self.items = []
