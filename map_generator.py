import random
from parser import Parser


class Generator:
    
    def __init__(self):
        self.size = 0
        
    def generator(self):
        self.size = int(input("Enter the map size: "))
        if self.size < 3:
            print("Puzzle size can not be lower than 3.")
            self.generator()
        f = open("generated_map.txt", 'w')
        f.write("# Generated map\n")
        f.write(str(self.size) + "\n")
        numbers = random.sample(range(self.size**2), self.size**2)
        for i in range(self.size):
            for j in range(self.size):
                f.write(str(numbers[self.size * i + j]))
                f.write(" ")
            f.write('\n')
        
                
            
if __name__ == '__main__':
    gen = Generator()
    gen.generator()