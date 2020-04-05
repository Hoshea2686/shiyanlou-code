# /usr/bin/python3
# -*-coding:utf-8-*-
# 图片转字符画的小工具
# pillow, argparse, linux命令行操作， python基础

import argparse
from PIL import Image

# 先实例化一个parser对象
parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-o", "--output", type=str, default="output.txt")
parser.add_argument("--width", type=int, default=80)
parser.add_argument("--height", type=int, default=80)
args = parser.parse_args()
print(args)
IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

char_set = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 定义一个函数将一个彩色对应到一个字符
def color2char(r, g, b, alpha=256):
	if alpha == 0:
		return ' '
	gray = int(0.2126*r+0.7152*g+0.0722*b)
	unit = len(char_set)/256
	return char_set[int(gray*unit)]

if __name__ == "__main__":
	im = Image.open(IMG)
	im = im.resize((WIDTH,HEIGHT), Image.NEAREST)
	txt = ""
	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt += color2char(*im.getpixel((j, i)))
		txt += '\n'
	print(txt)
	
	with open(OUTPUT, 'w') as f:
		f.write(txt)
		




