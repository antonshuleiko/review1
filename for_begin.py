import globals
def begin():
    for i in range(2 * globals.Globals.sizex - 1):  # матрица со стенами
        globals.Globals.visits_with_walls_matrix.append([])  # теперь везде стены
        for k in range(2 * globals.Globals.sizey - 1):
            globals.Globals.visits_with_walls_matrix[i].append(0)
    xwal, ywal = 0, 0
