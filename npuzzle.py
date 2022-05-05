import sys
import math

from pandas import to_numeric

class Npuzzle:
    def __init__(self):
        self.map = []
        
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
            print(flat_map)
            for i in range(array_size**2):
                if i % array_size == 0:
                    self.map.append(flat_map[i:array_size + i])
            print(self.map)
            
npuzzle = Npuzzle()
npuzzle.map_parser()