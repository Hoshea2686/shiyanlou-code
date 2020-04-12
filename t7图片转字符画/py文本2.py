# /urs/bin/python3
# -*-coding:utf-8-*-

from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-o', '--output', type=str, default='output.txt')
args = parser.parse_args()
IMG = args.file
OUTPUT = args.output
WIDTH = 80
HEIGHT = 80

char_set = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def color2char(r, g, b, alpha):
	if alpha == 0:
		return ' '
	gray = int(0.2126*r+0.7152*g+0.0722*b)
	uint = len(char_set)/256.0
	return char_set[int(gray * uint)]

if __name__ == '__main__':
	im = Image.open(IMG)
	im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
	txt = ''
	for i in range(WIDTH):
		for j in range(HEIGHT):
			color = im.getpixel((j, i))
			txt += color2char(*color)
		txt += '\n'
	print(txt)
	with open(OUTPUT, 'w') as f:
		f.write(txt)
