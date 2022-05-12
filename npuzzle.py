from ctypes import addressof
from email.headerregistry import Address
from re import L, template
import sys
import math
import numpy as np
from pandas import to_numeric

class Astar:
    def __init__(self, node):
        self.start = node
        self.open = []
        self.closed = []
        self.N = 0
        self.depth = 0
        
    def check_in_closed(self, node):
        for map_closed in self.closed:
            if (map_closed.map == node.map).all():
                return 0
        return 1

    def check_in_open(self, node):
        for map_open in self.open:
            if (map_open.map == node.map).all() and node.total_cost > map_open.total_cost:
                return 0
        return 1
        
    def algo(self):
        self.open.append(self.start)
        while len(self.open) != 0:
            tmp = []
            tmp_to_pop = []
            for index, node in enumerate(self.open):
                if node.heuristic_value == 0:
                    self.closed.append(node)
                for child in node.children:
                    if self.check_in_closed(child) and self.check_in_open(child):
                        tmp.append(child)
                tmp_to_pop.append(index)
                self.closed.append(node)
            for i in tmp_to_pop:
                self.open.pop(i)
            for node in tmp:
                self.open.append(node)
            print("coucou twe")
        print(self.closed[len(self.closed) - 1].map)
            
class Npuzzle:
    def __init__(self, map, heuristic, cost, parent, goal_map, total_cost):
        self.map = map
        self.cost_so_far = cost
        self.heuristic_value = heuristic
        self.children = []
        self.parent = parent
        self.goal_map = goal_map
        self.total_cost = total_cost
        
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

    def get_heuristic(self, actual_map):
        heuristic = 0
        for index, i in enumerate(self.goal_map):
            for index1, j in enumerate(i):
                for idx, y in enumerate(actual_map):
                    for idx1, x in enumerate(y):
                        if (x == j and x != 0):
                            heuristic += (abs((index - idx) + (index1 - idx1)))
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
        
    def check_duplicate(self, map):
        tmp = self
        while tmp.parent != False:
            if (map == tmp.map).all():
                return False
            tmp = tmp.parent
        return True
        
    def find_blank_space(self):
        for y, i in enumerate(self.map):
            for x, j in enumerate(i):
                if (j == 0):
                    return [y, x]
    
    def move(self, pos, new_pos):
        try:
            tmp_map = np.array(self.map)
            tmp = self.map[new_pos[0]][new_pos[1]]
            tmp_map[new_pos[0]][new_pos[1]] = 0
            tmp_map[pos[0]][pos[1]] = tmp
        except:
            return 0
        return tmp_map
        
    def create_node(self):
        
        space = self.find_blank_space()
        move = self.move(space, [space[0], space[1] - 1])

        if space[1] != 0 and self.check_duplicate(move):
            self.children.append(Npuzzle(move, self.get_heuristic(move), self.cost_so_far + 1, self, self.goal_map, self.get_heuristic(move) + self.cost_so_far + 1))
        
        move = self.move(space, [space[0], space[1] + 1])
        if space[1] != len(self.map) - 1 and self.check_duplicate(move):
            self.children.append(Npuzzle(move, self.get_heuristic(move), self.cost_so_far + 1, self, self.goal_map, self.get_heuristic(move) + self.cost_so_far + 1))
        
        move = self.move(space, [space[0] - 1, space[1]])
        if space[0] != 0 and self.check_duplicate(move):
            self.children.append(Npuzzle(move, self.get_heuristic(move), self.cost_so_far + 1, self, self.goal_map, self.get_heuristic(move) + self.cost_so_far + 1))
        
        move = self.move(space, [space[0] + 1, space[1]])
        if space[0] != len(self.map) - 1 and self.check_duplicate(move):
            self.children.append(Npuzzle(move, self.get_heuristic(move), self.cost_so_far + 1, self, self.goal_map, self.get_heuristic(move) + self.cost_so_far + 1))
    
npuzzle = Npuzzle([], 0, 0, False, [], 0)
npuzzle.map_parser()
npuzzle.generate_goal_map()
npuzzle.heuristic_value = npuzzle.get_heuristic(npuzzle.map)
npuzzle.create_node()
npuzzle.total_cost = npuzzle.heuristic_value + npuzzle.cost_so_far
algo = Astar(npuzzle)
algo.algo()