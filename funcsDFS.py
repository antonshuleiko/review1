import globals
import pygame
import random
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
        return -2, -2, -2, -2

def maze_generate(n=globals.Globals.sizex, m=globals.Globals.sizey):
    global xwal, ywal
    was_here_matrix, with_walls_matrix = [], []
    for i in range(n):   #создаем матрицу клеток, которые посещали
        was_here_matrix.append([])
        for k in range(m):
            was_here_matrix[i].append(0)
    for i in range(2 * n - 1):                       # матрица со стенами
        with_walls_matrix.append([])               #0 - стена, 1 - место для хода
        for k in range(2 * m - 1):
            if i % 2 == 0 and k % 2 == 0:
                with_walls_matrix[i].append(1)
            else:
                with_walls_matrix[i].append(0)
    x0, y0 = 0, 0
    globals.Globals.visits = [(x0, y0)]        # список клеток, где были, по порядку
    was_here_matrix[x0][y0] = 1     # матрица клеток, где были
    x, y, xwal, ywal = go_to_neighbors(x0, y0, was_here_matrix)
    for i in range(1, n * m):
        while not (x >= 0 and y >= 0):    #если нет соседей, то берем предыдущую клетку
            x, y = globals.Globals.visits[-1]
            globals.Globals.visits.pop()
            x, y, xwal, ywal = go_to_neighbors(x, y, was_here_matrix)
        globals.Globals.visits.append((x, y))
        globals.Globals.visits_with_walls_matrix[2 * x][2 * y] = 1
        globals.Globals.visits_with_walls_matrix[xwal][ywal] = 1
        was_here_matrix[x][y], with_walls_matrix[xwal][ywal] = 1, 1
        x, y, xwal, ywal = go_to_neighbors(x, y, was_here_matrix)
    return with_walls_matrix


def draw(matrix_walls, width_line=5, width_walls=5, color_all_way=(255, 255, 255),
         color_wall=(0, 0, 0), border=3, color_true_way=(255, 0, 0)):
    height = border * 2 + width_line * (len(matrix_walls[0]) // 2 + 1) + width_walls * (len(matrix_walls[0]) // 2)
    width = border * 2 + width_line * (len(matrix_walls) // 2 + 1) + width_walls * (len(matrix_walls) // 2)
    pygame.init()
    window = pygame.display.set_mode((width, height))
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
                    if matrix_walls[x][y]:
                        pygame.draw.line(window, color_all_way, [i, j], [i, j], 1)
                    else:
                        pygame.draw.line(window, color_wall, [i, j], [i, j], 1)

    pygame.display.update()
    pygame.image.save(window, 'save1.png')
    pygame.time.wait(globals.Globals.WAIT1)
    pygame.image.load('save0.png')
    pygame.time.wait(globals.Globals.WAIT2)
