from operator import attrgetter
import sys
import math
import numpy as np
from pandas import to_numeric
from node import Node
from  parser import Parser
from heuristic import *
from visualizer import *

class Npuzzle:
    def __init__(self, size):
        self.map = []
        self.size = size

    @staticmethod
    def map_to_str(map):
        res = ""
        for i in map:
            res += str(i)
        return res
    
    
    @staticmethod
    def move(map, pos, new_pos):
        try:
            tmp_map = np.array(map)
            tmp = map[new_pos]
            tmp_map[new_pos] = 0
            tmp_map[pos] = tmp
        except:
            return []
        return tmp_map


    def generate_children(self, map, parent):

        children = []
        blank_space = np.where(map == 0)[0][0]

        pos = Npuzzle.move(map, blank_space, blank_space + 1)
        if (blank_space + 1) % self.size != 0:
            children.append(Node(pos, self.map_to_str(pos), parent))

        pos = Npuzzle.move(map, blank_space, blank_space - 1)
        if blank_space % self.size != 0:
            children.append(Node(pos, self.map_to_str(pos), parent))

        pos = Npuzzle.move(map, blank_space, blank_space - self.size)
        if blank_space >= self.size:
            children.append(Node(pos, self.map_to_str(pos), parent))
        
        pos = Npuzzle.move(map, blank_space, blank_space + self.size)
        if blank_space + self.size < len(map):
            children.append(Node(pos, self.map_to_str(pos), parent))
        return children

    def check_dict(self, openDict, child):
        if child.id in openDict:
            return openDict[child.id].total_cost < child.total_cost
        return False

    def check_in_closed(self, closedDict, child):
        if child.id in closedDict:
            return True
        return False

def astar(start, end, size):
    npuzzle = Npuzzle(size)
    start_node = Node(start, Npuzzle.map_to_str(start))
    end_node = Node(end)
    
    start_node.cost_so_far = start_node.heuristic = start_node.total_cost = 0
    end_node.cost_so_far = end_node.heuristic = end_node.total_cost = 0

    open_list = []
    open_dict = {}
    closed_list = []
    closed_dict = {}
    open_list.append(start_node)

    while len(open_list) != 0:
        current_node = min(reversed(open_list),key=attrgetter('total_cost'))
        open_list.pop(open_list.index(current_node))
        closed_list.append(current_node)
        closed_dict[current_node.id] = current_node

        if np.equal(current_node.map, end_node.map).all():
            print(current_node)
            path = []
            current = current_node
            while current is not None:
                path.append(current.map)
                current = current.parent
            open_list.clear()
            closed_list.clear()
            open_dict.clear()
            closed_dict.clear()
            return path[::-1]

        children = npuzzle.generate_children(current_node.map, current_node)
        print("Current node heuristic:",current_node.heuristic)
        for child in children:

            if npuzzle.check_in_closed(closed_dict, child):
                continue
            
            child.cost_so_far = current_node.cost_so_far + 1
            child.heuristic = linear_conflicts(child.map, end_node.map, size)
            child.total_cost = child.cost_so_far // size + child.heuristic

            if npuzzle.check_dict(open_dict, child):
                continue

            open_list.append(child)
            open_dict[child.id] = child


if __name__ == '__main__':
    parser = Parser()
    parser.map_parser()
    parser.generate_goal_map()

    algo = astar(parser.map, parser.goal_map, parser.size)
    for i in algo:
        print(i)
    visualizer(algo)

