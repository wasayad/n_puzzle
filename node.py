class Node:
    def __init__(self, map = [], id = "", parent = None, position = None):
          
        self.map = map
        self.id = id
        self.parent = parent
        self.position = position
        self.cost_so_far = 0
        self.heuristic = 0
        self.total_cost = 0