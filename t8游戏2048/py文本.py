# /urs/bin/python3
# -*-coding:utf-8-*-

import random
import curses
from itertools import chain


UP = 'up'
LEFT = 'left'
DOWN = 'down'
RIGHT = 'right'
RESTART = 'restart'
EXIT = 'exit'

class Action(object):

    letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
    actions = [UP, LEFT, DOWN, RIGHT, RESTART, EXIT]
    actions_dict = dict(zip(letter_codes, actions * 2))

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get(self):
        char = "N"
        while char not in self.actions_dict:
            char = self.stdscr.getch()
        return self.actions_dict[char]

class Grid(object):

    def __init__(self, size):
        self.size = size
        self.cells = None
        self.reset()

    def reset(self):
        self.score = 0
        self.cells = [[0 for i in range(self.size)] for j in range(self.size)]
        self.add_random_item()
        self.add_random_item()

    def add_random_item(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
        (i, j) = random.choice(empty_cells)
        self.cells[i][j] = 4 if random.randrange(100) >= 90 else 2

    @staticmethod
    def transpose(matix):
        return [list(row) for row in zip(*matix)]

    @staticmethod
    def invert(matix):
        return [row[::-1] for row in matix]

    def move_row_left(self, row):
        def tighten(row):
            new_row = [i for i in row if i != 0]
            new_row += [0 for i in range(len(row) - len(new_row))]
            return new_row

        def merge(row):
            pair = False
            new_row = []
            for i in range(len(row)):
                if pair:
                    new_row.append(2 * row[i])
                    self.score += 2 * row[i]
                    pair = False
                else:
                    if i + 1 < len(row) and row[i] == row[i + 1]:
                        pair = True
                        new_row.append(0)
                    else:
                        new_row.append(row[i])
            assert len(new_row) == len(row)
            return new_row
        return tighten(merge(tighten(row)))

    def move(self, direction):
        moves = {}
        moves[LEFT]  = lambda matix: [self.move_row_left(row) for row in matix]
        moves[RIGHT] = lambda matix: self.invert(moves[LEFT](self.invert(matix)))
        moves[UP]    = lambda matix: self.transpose(moves[LEFT](self.transpose(matix)))
        moves[DOWN]  = lambda matix: self.transpose(moves[RIGHT](self.transpose(matix)))
        if direction in moves and self.check_move(direction):
            self.cells = moves[direction](self.cells)
            self.add_random_item()
            return True
        return False

    def row_is_left_movable(self, row):
            '''判断一行里面能否有元素进行左移动或合并
            '''
            def change(i):
                # 当左边有空位（0），右边有数字时，可以向左移动
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                # 当左边有一个数和右边的数相等时，可以向左合并
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

    def check_move(self, direction):
        # 检查能否移动（合并也可以看作是在移动）
        check = {}
        # 判断矩阵每一行有没有可以左移动的元素
        check[LEFT]  = lambda matix: any(self.row_is_left_movable(row) for row in matix)
        # 判断矩阵每一行有没有可以右移动的元素。这里只用进行判断，所以矩阵变换之后，不用再变换复原
        check[RIGHT] = lambda matix: check[LEFT](self.invert(matix))

        check[UP]    = lambda matix: check[LEFT](self.transpose(matix))

        check[DOWN]  = lambda matix: check[RIGHT](self.transpose(matix))

        # 如果 direction 是“左右上下”即字典 check 中存在的操作，那就执行它对应的函数
        if direction in check:
            # 传入矩阵，执行对应函数 
            return check[direction](self.cells)
        return False

class Screen(object):

    help_string1 = '(W)up (S)down (A)left (D)right'
    help_string2 = '     (R)Restart (Q)Exit'
    over_string = '           GAME OVER'
    win_string = '          YOU WIN!'

    def __init__(self, screen=None, cells=None, score=0, best_score=0, over=False, win=False):
        self.cells = cells  # 一个矩阵
        self.score = score # 分数int
        self.over = over  # 
        self.win = win
        self.screen = screen

    def cast(self, string):
        self.screen.addstr(string + '\n')

    def draw_row(self, row):
        self.cast(''.join('|{: ^5}'.format(num) if num > 0 else '|     ' for num in row) + '|')

    def draw(self):
        self.screen.clear()
        # 分数
        self.cast('SCORE: ' + str(self.score))
        # 网格和网格中数值
        for row in self.cells:
            self.cast('+-----' * len(self.cells) + '+')
            self.draw_row(row)
        self.cast('+-----' * len(self.cells) + '+')

        # 帮助提示文字
        if self.win:
            self.cast(self.win_string)
        else:
            if self.over:
                self.cast(self.over_string)
            else:
                self.cast(self.help_string1)

        self.cast(self.help_string2)


class GameManager(object):

    def __init__(self, size=4, win_num=32):
        self.size = size
        self.win_num = win_num
        self.reset()

    def reset(self):
        self.state = 'init'
        self.win = False
        self.over = False
        self.score = 0
        self.grid = Grid(self.size)
        self.grid.reset()

    @property
    def screen(self):
        return Screen(screen=self.stdscr, score=self.score, cells=self.grid.cells, win=self.win, over=self.over)

    @property
    def is_win(self):
        self.win = max(chain(*self.grid.cells)) >= self.win_num
        return self.win

    @property
    def is_over(self):
        self.over = not any(self.grid.check_move(move) for move in self.action.actions)
        return self.over

    def state_init(self):
        self.reset()
        return 'game'

    def state_game(self):
        self.screen.draw()
        action = self.action.get()

        if action == RESTART:
            return 'init'
        if action == EXIT:
            return 'exit'
        if self.grid.move(action):
            self.score = self.grid.score
            if self.is_win:
                return 'win'
            if self.is_over:
                return 'over'
        return 'game'

    def state_win(self):
        self.screen.draw()
        action = self.action.get()

        if action == RESTART:
            return 'init'
        if action == EXIT:
            return 'exit'
        return 'win'

    def state_over(self):
        self.screen.draw()
        action = self.action.get()

        if action == Action.RESTART:
            return 'init'
        if action == Action.EXIT:
            return 'exit'
        return 'over'

    def __call__(self, stdscr):
        curses.use_default_colors()
        self.stdscr = stdscr
        self.action = Action(stdscr)
        while self.state != 'exit':
            self.state = getattr(self, 'state_' + self.state)()


if __name__ == '__main__':
    curses.wrapper(GameManager())