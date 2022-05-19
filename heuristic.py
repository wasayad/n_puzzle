import numpy as np

def manhattan_heuristic(size, actual_map, goal_map):
    heuristic = 0
        
    for index, row in enumerate(goal_map):
        val = np.where(row == actual_map)
        heuristic += abs(index // size - val[0][0] // size) + abs(index % size - val[0][0] % size)
    return heuristic
    
def tiles_out_of_place_heuristic(map, goal_map):
    heuristic = 0

    for idx, i in enumerate(goal_map):
        if i != map[idx]:
            heuristic += 1
    return heuristic
    
def linear_conflicts(candidate, solved, size):
    def count_conflicts(candidate_row, solved_row, size, ans=0):
        counts = [0 for x in range(size)]
        for i, tile_1 in enumerate(candidate_row):
            if tile_1 in solved_row and tile_1 != 0:
                solved_i = solved_row.index(tile_1)
                for j, tile_2 in enumerate(candidate_row):
                    if tile_2 in solved_row and tile_2 != 0 and i != j:
                        solved_j = solved_row.index(tile_2)
                        if solved_i > solved_j and i < j:
                            counts[i] += 1
                        if solved_i < solved_j and i > j:
                            counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            candidate_row[i] = -1
            ans += 1
            return count_conflicts(candidate_row, solved_row, size, ans)

    res = manhattan_heuristic(size, candidate, solved)
    candidate_rows = [[] for y in range(size)]
    candidate_columns = [[] for x in range(size)]
    solved_rows = [[] for y in range(size)]
    solved_columns = [[] for x in range(size)]
    for y in range(size):
        for x in range(size):
            idx = (y * size) + x
            candidate_rows[y].append(candidate[idx])
            candidate_columns[x].append(candidate[idx])
            solved_rows[y].append(solved[idx])
            solved_columns[x].append(solved[idx])
    for i in range(size):
        res += count_conflicts(candidate_rows[i], solved_rows[i], size)
    for i in range(size):
        res += count_conflicts(candidate_columns[i], solved_columns[i], size)
    return res
