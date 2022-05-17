from asyncio import sleep
from multiprocessing.sharedctypes import Value
from operator import attrgetter
import sys
import math
import numpy as np
from pandas import to_numeric

class Parser:
    def __init__(self):
        self.map = []
        self.goal_map = []
        self.size = 0

    def map_parser(self):
        # Parse the input file into a 2 dimensions tab
        with open(sys.argv[1], "r") as f:
            array_size = 0
            flat_map = ""
            for idx, line in enumerate(f):
                if idx == 1:
                    array_size = to_numeric(line)
                    self.size = to_numeric(line)
                elif idx > 1:
                    line = line.split("#")
                    if (len(line) > 1):
                        flat_map = flat_map.replace("\n", " ") + line[0]
                    else:
                        flat_map = flat_map.replace("\n", " ") + line[0]
            flat_map = flat_map.split(" ")
            for i in range(array_size**2):
                if i % array_size == 0:
                    self.map.append(flat_map[i:array_size + i])
            self.map.clear()
            for i in range(len(flat_map)):
                try:
                    self.map.append(int(flat_map[i]))
                except:
                    pass
            for i in range(self.size**2):
                if self.map.count(i) > 1:
                    print("Duplicate numbers !")
                    exit(1)
            self.map = np.array(self.map)

    def generate_goal_map(self):
        self.goal_map = np.zeros((self.size, self.size), int)
        size = self.size
        delimiter_x = 0
        delimiter_y = 0
        y = 0
        x = 0
        i = 1
        for j in range(self.size):
            x = delimiter_x - 1 

            while (x < size - delimiter_x - 1 and i != self.size**2):
                x += 1
                self.goal_map[y][x] = i
                i += 1
            y = delimiter_y
            while (y < size - delimiter_y - 1 and i != self.size**2):
                y += 1
                self.goal_map[y][x] = i
                i += 1
            while (x > delimiter_x and i != self.size**2):
                x -= 1
                self.goal_map[y][x] = i
                i += 1
            while (y > delimiter_y + 1 and i != self.size**2):
                y -= 1
                self.goal_map[y][x] = i
                i += 1
            delimiter_x += 1
            delimiter_y += 1
        flat_goal_map = []
        for i in self.goal_map:
            for j in i:
                flat_goal_map.append(j)
        self.goal_map = np.array(flat_goal_map)
        
    def get_taxicab_distance(self, puzzle, solved, size):
        pi = puzzle.index(0)
        p1, p2 = pi // size, pi % size
        qi = solved.index(0)
        q1, q2 = qi // size, qi % size
        return abs(p1 - q1) + abs(p2 - q2)


    def count_inversions(self, puzzle, solved, size):
        res = 0
        for i in range(size * size - 1):
            for j in range(i + 1, size * size):
                vi = puzzle[i]
                vj = puzzle[j]
                if solved.index(vi) > solved.index(vj):
                    res += 1
        return res


    def is_solvable(self, puzzle, solved, size):
        taxicab_distance = self.get_taxicab_distance(puzzle, solved, size)
        num_inversions = self.count_inversions(puzzle, solved, size)
        return taxicab_distance % 2 == num_inversions % 2