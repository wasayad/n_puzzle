from distutils.log import error
import operator
import sys
import math
import numpy as np
from pandas import to_numeric

class Node:
   def __init__(self, map = [], parent = None, position = None):
          
          self.map = map

          self.parent = parent
          self.position = position

          self.cost_so_far = 0
          self.heuristic = 0
          self.total_cost = 0
        

            
class Npuzzle:
    def __init__(self, goal_map):
        self.map = []
        self.goal_map = goal_map
        
    def map_parser(self):
        # Parse the input file into a 2 dimensions tab
        with open(sys.argv[1], "r") as f:
            array_size = 0
            flat_map = ""
            for idx, line in enumerate(f):
                if idx == 1:
                    array_size = to_numeric(line)
                elif idx > 1:
                    flat_map = flat_map.replace("\n", " ") + line
            flat_map = flat_map.split(" ")
            for i in range(array_size**2):
                if i % array_size == 0:
                    self.map.append(flat_map[i:array_size + i])    
            self.map = [list(map(int, i)) for i in self.map]
            self.map = np.array(self.map)

    def get_heuristic(self, actual_map, goal_map):
        heuristic = 0
        for index, i in enumerate(goal_map):
            for index1, j in enumerate(i):
                for idx, y in enumerate(actual_map):
                    for idx1, x in enumerate(y):
                        if (x == j and x != 0):
                            heuristic += (abs(index - idx) + abs(index1 - idx1))
        return heuristic

    def generate_goal_map(self):
        self.goal_map = np.zeros((len(self.map), len(self.map)), int)
        size = len(self.map)
        delimiter_x = 0
        delimiter_y = 0
        y = 0
        x = 0
        i = 1
        for j in range(len(self.map)):
            x = delimiter_x - 1 

            while (x < size - delimiter_x - 1 and i != len(self.map)**2):
                x += 1
                self.goal_map[y][x] = i
                i += 1
            y = delimiter_y
            while (y < size - delimiter_y - 1 and i != len(self.map)**2):
                y += 1
                self.goal_map[y][x] = i
                i += 1
            while (x > delimiter_x and i != len(self.map)**2):
                x -= 1
                self.goal_map[y][x] = i
                i += 1
            while (y > delimiter_y + 1 and i != len(self.map)**2):
                y -= 1
                self.goal_map[y][x] = i
                i += 1
            delimiter_x += 1
            delimiter_y += 1
        
    def find_blank_space(self, map):
        for y, i in enumerate(map):
            for x, j in enumerate(i):
                if (j == 0):
                    return [y, x]
    
    def move(self, map, pos, new_pos):
        try:
            tmp_map = np.array(map)
            tmp = map[new_pos[0]][new_pos[1]]
            tmp_map[new_pos[0]][new_pos[1]] = 0
            tmp_map[pos[0]][pos[1]] = tmp
        except:
            return []
        return tmp_map

    def generate_children(self, map):

        children = []
        blank_space = self.find_blank_space(map)

        pos = self.move(map, blank_space, [blank_space[0], blank_space[1] - 1])
        if blank_space[1] != 0 and len(pos):
            children.append(Node(pos))
        
        pos = self.move(map, blank_space, [blank_space[0], blank_space[1] + 1])
        if blank_space[1] != len(map) - 1 and len(pos):
            children.append(Node(pos))

        pos = self.move(map, blank_space, [blank_space[0] - 1, blank_space[1]])
        if blank_space[0] != 0 and len(pos):
            children.append(Node(pos))
        
        pos = self.move(map, blank_space, [blank_space[0] + 1, blank_space[1]])
        if blank_space[0] != len(map) - 1 and len(pos):
            children.append(Node(pos))

        return children


def astar(map, start, end):

    npuzzle = Npuzzle([])
      
    start_node = Node(start)
    start_node.cost_so_far = start_node.heuristic = start_node.total_cost = 0
    end_node = Node(end)
    end_node.cost_so_far = end_node.heuristic = end_node.total_cost = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) != 0:
          
        current_node = open_list[0]
        current_index = 0

        for index, i in enumerate(open_list):
            if i.total_cost < current_node.total_cost:
                current_node = i
                current_index = index
      
        open_list.pop(current_index)
        closed_list.append(current_node)
        #open_list = sorted(open_list, key=operator.attrgetter('total_cost'))

        print(current_node.map)
        print("\n")
        if (current_node.map == end_node.map).all():
            print("GG")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        children = npuzzle.generate_children(current_node.map)

        for child in children:

            try:
                for closed_child in closed_list:
                    if (child.map == closed_child.map).all():
                        raise Exception
            except Exception:
                continue
            
            child.cost_so_far = current_node.cost_so_far + 1
            child.heuristic = npuzzle.get_heuristic(child.map, end_node.map)
            child.total_cost = child.cost_so_far + child.heuristic

            try:
                for open_node in open_list:
                    if (child.map == open_node.map).all() and child.cost_so_far > open_node.cost_so_far:
                        raise Exception
            except Exception:
                continue
            open_list.append(child)


    
npuzzle = Npuzzle([])
npuzzle.map_parser()
npuzzle.generate_goal_map()

start = npuzzle.map
end = npuzzle.goal_map

algo = astar(npuzzle.map, start, end)
