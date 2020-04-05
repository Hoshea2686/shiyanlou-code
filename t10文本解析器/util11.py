# /urs/bin/python3
# -*-coding:utf-8-*-


def lines(file):
	"""
	给file生成器添加一空行

	file: 为文件的生成器， 如：file = open('test.txt')
	返回：file中的每一行。
	"""
	for line in file:
		yield line 
	yield '/n' # 最后添加空一行

def blocks(file):
	"""
	将file块，取出来。获取前后空行之间的内容（块）
	"""
	block = []
	for line in lines(file):
		if line.strip():
			block.append(line)
		elif block:
			yield ''.join(block).strip()
			block = []

if __name__ == '__main__':
	with open('test1.txt') as f:
		for l in blocks(f):
			print(l)

