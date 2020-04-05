# /urs/bin/python3
# -*-coding:utf-8-*-
# copy pic2char2.py

import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o', '--output', type=str, default='output.txt')
args = parser.parse_args()
print(args)
FILE = args.file
OUTPUT = args.output

WIDTH = 80
HEIGHT = 80
CHARSET = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def color2char(r, g, b, alpha=256):
	if alpha == 0:
		return ' '
	gray = int(0.2126*r+0.7152*g+0.0722*b)
	unit = len(CHARSET)/256.0
	return CHARSET[int(gray * unit)]

if __name__ == '__main__':
	im = Image.open(FILE)
	im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
	txt = ""
	# 获取图片中的像素点
	for i in range(HEIGHT):
		for j in range(WIDTH):
			color = im.getpixel((j, i))
			# 将颜色转化为字符串
			txt += color2char(*color)
		txt += '\n'
	print(txt)

	with open(OUTPUT, 'w') as f:
		f.write(txt)
