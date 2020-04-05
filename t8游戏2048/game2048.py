# /usr/bin/python3
# -*-coding:utf-8-*-
# 2048游戏。
# 状态机， 列表推倒式， 匿名函数lambda， curses终端模式(游戏运行在此模式下)

import  curses
from random import randrange, choice

# 定义行为
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
# 定义按键
buttons = [ord(ch) for ch in "wasdrqWASDRQ"]	# ord()获得字母的ascii值
# 关联行为和按键
button_actions = dict(zip(buttons, actions * 2))
# print(button_actions)

# 获取用户行为(循环+阻塞)
def get_action(keyboard):
	button = -1
	while button not in button_actions:
		button = keyboard.getch()	# 获取按键的ascii值
	return button_actions[button]

# 矩阵转置
def transpose(matix):
	return [list(row) for row in zip(*matix)]

# 矩阵左右反序
def invert(matix):
	return [row[::-1] for row in matix]



# 一个游戏类
class GameField(object):
	def __init__(self, size=4, win_score=128):
		self.size = size
		self.win_score = win_score
		self.score = 0
		self.best_score = 0
		self.reset()
	
	def reset(self):
		if self.best_score < self.score:
			self.best_score = self.score
		self.score = 0
		self.field = [[0 for i in range(self.size)] for j in range(self.size)]
		self.spawn()
		self.spawn()
	
	def spawn(self):
		num = 4 if randrange(100) > 89 else 2
		(i, j) = choice([(i, j) for i in range(self.size) for j in range(self.size) if self.field[i][j] == 0])
		self.field[i][j] = num

	def move(self, direction):
		def row_left(old_row):
			def merge(row):
				i = 0
				new_row = []
				while i < len(row):
					if i+1<len(row) and row[i] == row[i+1]:
						new_row += [0, 2*row[i]]
						self.score += 2*row[i]
						i += 2
					else:
						new_row += [row[i]]
						i += 1
				return new_row

			def shrink(row):
				new_row = [num for num in row if num != 0]
				new_row += [0 for i in range(len(row) - len(new_row))]
				return new_row

			return shrink(merge(shrink(old_row)))
		
		# 定义一个moves， 存放移动方向，和移动函数
		moves = {}
		moves["Left"] = lambda field: [row_left(row) for row in field]
		moves["Right"] = lambda field: invert(moves["Left"](invert(field)))
		moves["Up"] = lambda field: transpose(moves["Left"](transpose(field)))
		moves["Down"] = lambda field: transpose(moves["Right"](transpose(field)))
		
		# 判断是否能移动
		if direction in moves and self.is_move(direction):
			self.field = moves[direction](self.field)
			self.spawn()
			return True
		return False

	def is_move(self, direction):
		def is_row_left(row):
			def change(i):
				# 判断每一个位置的数(从第二个数开始)与前一个数是否相等， 或者前一个数为0， 即能移动
				if row[i] == row[i-1] or row[i-1] == 0:
					return True
				return False
			return any((change(i) for i in range(1, len(row))))
		is_moves = {}
		is_moves["Left"] = lambda field: any((is_row_left(row) for row in field))
		is_moves["Right"] = lambda field: is_moves["Left"](invert(field))
		is_moves["Up"] = lambda field: is_moves["Left"](transpose(field))
		is_moves["Down"] = lambda field: is_moves["Right"](transpose(field))

		if direction in is_moves:
			return is_moves[direction](self.field)
		return False

	# 判断输赢
	def is_defeat(self):
		return not any((self.is_move(action) for action in actions))

	def is_win(self):
		return any((self.field[i][j]>=self.win_score for i in range(self.size) for j in range(self.size)))	

	def draw(self, screen):
		move_str = "(W)Up (S)Down (A)Left (D)Right"
		global_str = "     (R)Restart (Q)Exit"
		defeat_str = "          GAME OVER"
		win_str = "          YOU WIN!"

		def cast(txt):
			screen.addstr(txt + '\n')

		def hor_line():
			cast('+-----'*self.size + '+')

		def ver_line(row):
			cast(''.join('|{: ^5}'.format(num) if num > 0 else '|     ' for num in row) + '|')

		screen.clear()
		cast("Score: {}".format(self.score))
		cast("Best Score: {}".format(self.best_score))

		for row in self.field:
			hor_line()
			ver_line(row)
		hor_line()

		cast(global_str)
		if self.is_win():
			cast(win_str)
		elif self.is_defeat():
			cast(defeat_str)
		else:
			cast(move_str)
			

# 主逻辑
def main(stdscr):
	def init():
		# 显示相应的界面
		gamefield.reset()
		return "Game"
	
	def game():
		# 显示相应的界面
		gamefield.draw(stdscr)
		action = get_action(stdscr)
		if action == "Restart":
			return "Init"
		if action == "Exit":
			return "Exit"
		if gamefield.move(action):
			if gamefield.is_win():
				return "Win"
			if gamefield.is_defeat():
				return "Defeat"
		return "Game"

	def win():
		# 显示相应的界面
		gamefield.draw(stdscr)
		action = get_action(stdscr)
		if action == "Restart":
			return "Init"
		if action == "Exit":
			return "Exit"
		return "Win"
	
	def defeat():
		# 显示相应的界面
		gamefield.draw(stdscr)
		action = get_action(stdscr)
		if action == "Restart":
			return "Init"
		if action == "Exit":
			return "Exit"
		return "Defeat"
	
	gamefield = GameField()

	state_func = {
		"Init": init,
		"Game": game,
		"Win": win,
		"Defeat": defeat
	}

	state = "Init"
	while state != "Exit":
		state = state_func[state]()
curses.wrapper(main)
