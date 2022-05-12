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

    def generateMatrix(self, n):
            row1 = 0
            col1 = 0
            row2 = n
            col2 = n
            result = [ [0 for i in range(n)] for j in range(n)]
            num = 1
            while num<=n**2:
               for i in range(col1,col2):
                  result[row1][i] = num
                  num+=1
               if num > n**2:
                  break
               for i in range(row1+1,row2):
                  result[i][col2-1] = num
                  num+=1
               if num > n**2:
                  break
               for i in range(col2-2,col1-1,-1):
                  result[row2-1][i] = num
                  num+=1
               if num > n**2:
                  break
               for i in range(row2-2,row1,-1):
                  result[i][col1] = num
                  num+=1
                  row1+=1
                  row2-=1
                  col1+=1
                  col2-=1
                  #print(result)
            return result
            
npuzzle = Npuzzle()
npuzzle.map_parser()
print(npuzzle.generateMatrix(4))