# /urs/bin/python3
# -*-coding:utf-8-*-


class Insperation:
	def __init__(self):
		self.what_to_exe = None
		self.stack = []
		self.val_dict = {}

	def LOAD_NAME(self, name):
		value = self.val_dict[name]
		self.stack.append(value)

	def STORE_NAME(self, name):
		value = self.stack.pop()
		self.val_dict[name] = value

	def LOAD_VALUE(self, value):
		self.stack.append(value)

	def ADD_TWO_VALUES(self):
		num1 = self.stack.pop()
		num2 = self.stack.pop()
		total = num1 + num2
		self.stack.append(total)

	def PRINT_VALUE(self):
		result = self.stack.pop()
		print(result)

	def Parse(self, step):
		instrection, index = step
		if instrection in ['LOAD_NAME', 'STORE_NAME']:
			return self.what_to_exe['names'][index]
		elif instrection in ['LOAD_VALUE']:
			return self.what_to_exe['numbers'][index]

	def run_code(self, what_to_exe):
		self.what_to_exe = what_to_exe
		instrections = what_to_exe['instrections']
		for step in instrections:
			instrection, index = step
			method = getattr(self, instrection, None)
			if index is None:
				method()
			else:
				# arg = what_to_exe['numbers'][index]
				arg = self.Parse(step)
				method(arg)

if __name__ == '__main__':
	insperations = Insperation()
	# 3+7
	what_to_exe = {
		'instrections': [("LOAD_VALUE", 0),
						 ("LOAD_VALUE", 1),
						 ("ADD_TWO_VALUES", None),
						 ("PRINT_VALUE", None)],
		'numbers': [3, 7],
	}
	insperations.run_code(what_to_exe)
	'''
	def sub_():
		a=5
		b=9
		print(a+b)
	'''
	what_to_exe = {
		'instrections': [("LOAD_VALUE", 0),
						 ("STORE_NAME", 0),
						 ("LOAD_VALUE", 1),
						 ("STORE_NAME", 1),
						 ("LOAD_NAME", 0),
						 ("LOAD_NAME", 1),
						 ("ADD_TWO_VALUES", None),
						 ("PRINT_VALUE", None)],
		'numbers': [5, 9],
		'names': ['a', 'b']
	}
	insperations.run_code(what_to_exe)

