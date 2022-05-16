import globals
import random
def go_to_neighbors_prim(x, y, with_walls):
    neighbors_walls = []                                  #соседи - стены, за которыми мы не были
    xw, yw = 2 * x,  2 * y                            #координаты в матрице with_walls
    if xw > 0 and not with_walls[xw - 1][yw] and not with_walls[xw - 2][yw]:
        neighbors_walls.append((xw-1, yw))
    if xw < len(with_walls) - 2 and not with_walls[xw + 1][yw] and not with_walls[xw + 2][yw]:
        neighbors_walls.append((xw + 1,yw))
    if yw > 0 and not with_walls[xw][yw - 1] and not with_walls[xw][yw - 2]:
        neighbors_walls.append((xw, yw - 1))
    if yw < len(with_walls[0]) - 2 and not with_walls[xw][yw + 1] and not with_walls[xw][yw + 2]:
        neighbors_walls.append((xw,yw + 1))
    if neighbors_walls:
        #newx, newy = random.choice(neighbors_walls)
        xwal, ywal = random.choice(neighbors_walls)        #выбираем стен-соседей
        if xw == xwal:
            newx = x                                       #newx, newy - координаты новые в матрице без стен
            if ywal > yw:
                newy = y + 1
            else:
                newy = y - 1
        if yw == ywal:
            newy = y
            if xwal > xw:
                newx = x + 1
            else:
                newx = x - 1
        return newx, newy, xwal, ywal
    else:
        globals.Globals.false_way.add((xw, yw))
        return -1, -1, -1, -1

def maze_generate_prim(n=globals.Globals.sizex, m=globals.Globals.sizey):
    was_here_matrix, with_walls_matrix = [], []
    for i in range(n):   #создаем матрицу клеток, которые посещали
        was_here_matrix.append([])
        for k in range(m):
            was_here_matrix[i].append(0)
    for i in range(2 * n - 1):                       # матрица со стенами
        with_walls_matrix.append([])                 #теперь везде стены
        for k in range(2 * m - 1):
            with_walls_matrix[i].append(0)
    x, y = 0, 0
    with_walls_matrix[x * 2][y * 2], was_here_matrix[x][y]  = 1, 1 # матрица клеток, где были
    x, y, xwal, ywal = go_to_neighbors_prim(x, y, with_walls_matrix)
    for i in range(1, n * m):
        while not (x >= 0 and y >= 0):    #если нет соседей, то берем предыдущую клетку
            x, y = globals.Globals.visits[-1]
            globals.Globals.visits.pop()
            x, y, xwal, ywal = go_to_neighbors_prim(x, y, with_walls_matrix)
        globals.Globals.visits.append((x, y))
        was_here_matrix[x][y], with_walls_matrix[xwal][ywal] = 1, 1
        with_walls_matrix[x * 2][y * 2] = 1
        x, y, xwal, ywal = go_to_neighbors_prim(x, y, with_walls_matrix)
    return with_walls_matrix

