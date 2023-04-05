from Cell import Cell
import time
import random

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        if seed:
            random.seed(seed)
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visted()

    def _create_cells(self):
        for x in range(self._num_cols):
            self._cells.append([])
            for y in range(self._num_rows):
                cell = Cell(self._win)
                self._cells[x].append(cell)
        for x in range(self._num_cols):
            for y in range(self._num_rows):
                self._draw_cell(x, y)

    def _draw_cell(self, i, j):
        if self._win == None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.5)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols-1, self._num_rows-1)


    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            #right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            #left
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            #top
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            #bottom
            if j < self._num_rows -1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            next_cell = to_visit[random.randrange(len(to_visit))]

            if next_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            if next_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            if next_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            if next_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            self._break_walls_r(next_cell[0], next_cell[1])
        
    def _reset_cells_visted(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, x, y):
        self._animate()
        self._cells[x][y].visited = True
        if x == self._num_cols - 1 and y == self._num_rows - 1:
            return True
        
        #right
        if x < self._num_cols - 1 and not self._cells[x][y].has_right_wall and not self._cells[x+1][y].visited:
            self._cells[x][y].draw_move(self._cells[x+1][y])
            result = self._solve_r(x+1, y)
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x+1][y], True)
        #left
        if x > 0 and not self._cells[x][y].has_left_wall and not self._cells[x-1][y].visited:
            self._cells[x][y].draw_move(self._cells[x-1][y])
            result = self._solve_r(x-1, y)
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x-1][y], True)
        #top
        if y > 0 and not self._cells[x][y].has_top_wall and not self._cells[x][y-1].visited:
            self._cells[x][y].draw_move(self._cells[x][y-1])
            result = self._solve_r(x, y-1)
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y-1], True)
        #bottom
        if y < self._num_rows - 1 and not self._cells[x][y].has_bottom_wall and not self._cells[x][y+1].visited:
            self._cells[x][y].draw_move(self._cells[x][y+1])
            result = self._solve_r(x, y+1)
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y+1], True)

    def solve(self):
        self._solve_r(0, 0)
            
