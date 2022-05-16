import sys
class Globals:
    WAIT1 = 3000
    WAIT2 = 1000
    sizex = (int)(sys.argv[1])
    sizey = (int)(sys.argv[2])
    visits = [(0, 0)]  # список клеток, где были, по порядку
    visits_with_walls_matrix = []  # клетки со стенами
    false_way = set()