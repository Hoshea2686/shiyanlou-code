# /urs/bin/python3
# -*-coding:utf-8-*-

class Interperter:
	def __init__(self):
		self.stack = []		# 用来模拟堆栈
	def LOAD_VALUE(self, number):
		self.stack.append(number)
	def ADD_TWO_VALUES(self):
		first_num = self.stack.pop()	# pop()将stack中最后一个数取出来， stack也就少了一个数
		second_num = self.stack.pop()
		total = first_num + second_num
		self.stack.append(total)
	def PRINT_ANSWER(self):
		answer = self.stack.pop()
		print(answer)
	def run_code(self, what_to_execute):
		instructions = what_to_execute['instructions']
		numbers = what_to_execute['numbers']
		for step in instructions:
			instruction, argument = step
			if instruction == 'LOAD_VALUE':
				value = numbers[argument]
				self.LOAD_VALUE(value)
			if instruction == 'ADD_TWO_VALUES':
				self.ADD_TWO_VALUES()
			if instruction == 'PRINT_ANSWER':
				self.PRINT_ANSWER()

if __name__ == '__main__':
	interpreter = Interperter()
	what_to_execute = {
		"instructions": [("LOAD_VALUE", 0),
						("LOAD_VALUE", 1), 
						("ADD_TWO_VALUES", None),
						("PRINT_ANSWER", None)],		
		"numbers": [7, 5]
	}
	interpreter.run_code(what_to_execute)

	what_to_execute = {
		"instructions": [("LOAD_VALUE", 0),
						("LOAD_VALUE", 1), 
						("ADD_TWO_VALUES", None),
						("LOAD_VALUE", 2), 
						("ADD_TWO_VALUES", None),
						("PRINT_ANSWER", None)],		
		"numbers": [7, 5, 8]
	}
	interpreter.run_code(what_to_execute)