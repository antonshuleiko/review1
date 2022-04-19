import random
import pygame
import sys

sizex = (int)(sys.argv[1])
sizey = (int)(sys.argv[2])
visits = [(0, 0)]  # список клеток, где были, по порядку
visits_with_walls_matrix = []  # клетки со стенами
for i in range(2 * sizex - 1):        # матрица со стенами
    visits_with_walls_matrix.append([])  # теперь везде стены
    for k in range(2 * sizey - 1):
        visits_with_walls_matrix[i].append(0)
xwal, ywal = 0, 0

def go_to_neighbors(x, y, was_here):
    global xwal, ywal
    neighbors = []
    if x > 0 and not was_here[x - 1][y]:
        neighbors.append((x-1, y))
    if x < len(was_here) - 1 and not was_here[x + 1][y]:
        neighbors.append((x + 1,y))
    if y > 0 and not was_here[x][y - 1] :
        neighbors.append((x, y - 1))
    if y < len(was_here[0]) - 1 and not was_here[x][y + 1]:
        neighbors.append((x,y + 1))
    if neighbors:
        newx, newy = random.choice(neighbors)
        if x == newx:
            xwal = 2 * x
            if newy > y:
                ywal = newy * 2 - 1
            else:
                ywal = newy * 2 + 1
        if y == newy:
            ywal = 2 * y
            if newx > x:
                xwal = newx * 2 - 1
            else:
                xwal = newx * 2 + 1

        return newx, newy, xwal, ywal
    else:
        #visits_with_walls_matrix[xwal][ywal] = 0
        #visits_with_walls_matrix[x * 2][y * 2] = 0
        return -5, -5, -5, -5


def maze_generate(n=sizex, m=sizey):
    global xwal, ywal
    was_here_matrix = []
    for i in range(n):   #создаем матрицу клеток, которые посещали
        was_here_matrix.append([])
        for k in range(m):
            was_here_matrix[i].append(0)
    with_walls_matrix = []
    for i in range(2 * n - 1):                       # матрица со стенами
        with_walls_matrix.append([])               #0 - стена, 1 - место для хода
        for k in range(2 * m - 1):
            if i % 2 == 0 and k % 2 == 0:
                with_walls_matrix[i].append(1)
            else:
                with_walls_matrix[i].append(0)
    x0, y0 = 0, 0
    visits = [(x0, y0)]        # список клеток, где были, по порядку
    was_here_matrix[x0][y0] = 1     # матрица клеток, где были
    x, y, xwal, ywal = go_to_neighbors(x0, y0, was_here_matrix)
    for i in range(1, n * m):
        while not (x >= 0 and y >= 0):    #если нет соседей, то берем предыдущую клетку
            x, y = visits[-1]
            visits.pop()
            x, y, xwal, ywal = go_to_neighbors(x, y, was_here_matrix)
        visits.append((x, y))
        visits_with_walls_matrix[2 * x][2 * y] = 1
        visits_with_walls_matrix[xwal][ywal] = 1
        was_here_matrix[x][y] = 1
        with_walls_matrix[xwal][ywal] = 1
        x, y, xwal, ywal = go_to_neighbors(x, y, was_here_matrix)
    return with_walls_matrix

def draw(matrix_walls, width_line=5, width_walls=5, color_all_way=(255, 255, 255),
         color_wall=(0, 0, 0), border=3, color_true_way=(255, 0, 0)):
    height = border * 2 + width_line * (len(matrix_walls[0]) // 2 + 1) + width_walls * (len(matrix_walls[0]) // 2)
    width = border * 2 + width_line * (len(matrix_walls) // 2 + 1) + width_walls * (len(matrix_walls) // 2)
    pygame.init()
    window = pygame.display.set_mode((width, height))
    #while 1:
    for i in range(width):
        for j in range(height):
                if i < border or width - i <= border or j < border or height - j <= border:  # границы
                    pygame.draw.line(window, color_wall, [i, j], [i, j], 1)
                else:
                    x = (i - border) // (width_line + width_walls) * 2
                    y = (j - border) // (width_line + width_walls) * 2
                    if not (i - border) % (width_line + width_walls) <= width_line:
                        x += 1
                    if not (j - border) % (width_line + width_walls) <= width_line:
                        y += 1
                    if matrix_walls[x][y]:#and visits_with_walls_matrix[x][y]:
                        pygame.draw.line(window, color_all_way, [i, j], [i, j], 1)
                    #elif matrix_walls[x][y] and not visits_with_walls_matrix[x][y]:
                        #pygame.draw.line(window, color_all_way, [i, j], [i, j], 1)
                    else:
                        pygame.draw.line(window, color_wall, [i, j], [i, j], 1)

    pygame.display.update()
    pygame.image.save(window, 'save1.png')
    pygame.time.wait(3000)
    pygame.image.load('save0.png')
    pygame.time.wait(1000)

"""--------------------------------------------"""

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
        false_way.add((xw, yw))
        return -1, -1, -1, -1


def maze_generate_prim(n=sizex, m=sizey):
    was_here_matrix = []
    for i in range(n):   #создаем матрицу клеток, которые посещали
        was_here_matrix.append([])
        for k in range(m):
            was_here_matrix[i].append(0)
    with_walls_matrix = []
    for i in range(2 * n - 1):                       # матрица со стенами
        with_walls_matrix.append([])                 #теперь везде стены
        for k in range(2 * m - 1):
            with_walls_matrix[i].append(0)
    x0, y0 = 0, 0
    x, y = 0, 0
    with_walls_matrix[x * 2][y * 2] = 1
    was_here_matrix[x0][y0] = 1     # матрица клеток, где были
    x, y, xwal, ywal = go_to_neighbors_prim(x0, y0, with_walls_matrix)
    for i in range(1, n * m):
        while not (x >= 0 and y >= 0):    #если нет соседей, то берем предыдущую клетку
            x, y = visits[-1]
            visits.pop()
            x, y, xwal, ywal = go_to_neighbors_prim(x, y, with_walls_matrix)
        visits.append((x, y))
        was_here_matrix[x][y] = 1
        with_walls_matrix[xwal][ywal] = 1
        with_walls_matrix[x * 2][y * 2] = 1
        x, y, xwal, ywal = go_to_neighbors_prim(x, y, with_walls_matrix)

    return with_walls_matrix


false_way = set()
if sys.argv[3] == "DFS":
    matrix_walls = maze_generate()
    #print("________________________")
    #print(visits_with_walls_matrix)
    draw(matrix_walls)
elif sys.argv[3] == "Prim":
    matrix_walls = maze_generate_prim()
    draw(matrix_walls)




