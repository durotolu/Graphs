class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def earliest_ancestor(ancestors, starting_node):
    parents = []
    chilren = []
    for (parent_1, child_1) in ancestors:
        parents.append(parent_1)
        chilren.append(child_1)

    if starting_node not in chilren:
        return -1
    
    parent = starting_node

    q = Queue()
    q.enqueue(parent)
    visited = set()

    while q.size() > 0:
        v = q.dequeue()

        if v not in visited:
            visited.add(v)

            smallest = None
            for (i, j) in ancestors:
                if v == j:
                    smallest = i
                    break

            for (agba, omo) in ancestors:
                if omo == v:
                    if agba <= smallest:
                        q.enqueue(agba)
                        smallest = agba
    return v