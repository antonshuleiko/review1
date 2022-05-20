import for_begin
import funcsDFS
import funcsPrim

import sys
def main():
    for_begin.begin()
    if sys.argv[3] == "DFS":
        matrix_walls = funcsDFS.maze_generate()
        funcsDFS.draw(matrix_walls)
    elif sys.argv[3] == "Prim":
        matrix_walls = funcsPrim.maze_generate_prim()
        funcsDFS.draw(matrix_walls)