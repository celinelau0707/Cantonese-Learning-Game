# stack.py
class UndoManager:
    def __init__(self, max_steps=10):
        self.stack = []       
        self.max_steps = max_steps

    def push(self, state):
        if len(self.stack) >= self.max_steps:
            self.stack.pop(0)  
        self.stack.append(state) 

    def pop(self):
        return self.stack.pop() if not self.isEmpty() else None

    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

   

if __name__ == "__main__":
    manager = UndoManager(max_steps=3)
    states = [
        {"index": 0, "action": "A"},
        {"index": 1, "action": "B"},
        {"index": 2, "action": "C"}
    ]
    for s in states:
        manager.push(s)
    print("Stack after pushing 3 items:", manager.stack)
    popped = manager.pop()
    print("Popped item:", popped)  # output: {'index': 2, 'action': 'update'}
    print("Stack after pop:", manager.stack) #output: [{'index': 0, 'action': 'A'}, {'index': 1, 'action': 'B'}]
    manager.push({"index": 3, "action": "D"})
    manager.push({"index": 4, "action": "E"})
    print("Stack after pushing 2 more (max_steps=3):", manager.stack)#output: [{'index': 1, 'action': 'B'}, {'index': 3, 'action': 'D'}, {'index': 4, 'action': 'E'}]
    print("Is empty?", manager.isEmpty())  
    print("Current size:", manager.size())

