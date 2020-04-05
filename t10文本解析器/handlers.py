# /urs/bin/python3
# -*-coding:utf-8-*-

class Handler:

	test_getattr = "定义一个属性，测试getattr， 该函数返回一个对象的属性"
	def start_test(self):
		print("start_test")
	# 上面试测试用的

	def callback(self, prefix, name, *args):
		method = getattr(self, prefix + name, None)
		if callable(method):	# callable 内置函数， 用来判断参数对象是不是方法
			return method(*args)
	def start(self, name):
		self.callback('start_', name)

	def end(self, name):
		self.callback('end_', name)

	# 参数name 值为过滤器名字， 是字符串
	def sub(self, name):
		def substitution(match):
			result = self.callback('sub_', name, match)
			if result is None:
				result = match.group(0)
				# 正则表达式中，group（）用来提出分组截获的字符串，（）用来分组
				# group（1）表示正则中第一个括号中的内容。group（0）表示返回所有的分组，
			return result
		return substitution

class HTMLRenderer(Handler):

	# 以下各个方法分别在符合条件时被调用，打印标签或标签的 text 值

	def start_document(self):
		print('<html><head><title>ShiYanLou</title></head><body>')
	def end_document(self):
		print('</body></html>')
	def start_heading(self):
		print('<h2 style="color: #68BE5D;">')
	def end_heading(self):
		print('</h2>')
	def start_title(self):
		print('<h1 style="color: #1ABC9C;">')
	def end_title(self):
		print('</h1>')
	def start_paragraph(self):
		print('<p style="color: #444;">')
	def end_peragraph(self):
		print('</p>')
	def start_listitem(self):
		print('<li>')
	def end_listitem(self):
		print('</li>')
	def start_list(self):
        print('<ul style="color: #363736;">')
    def end_list(self):
        print('</ul>')
	def sub_emphasis(self, match):
		return ('<em>%s</em>' % match.group(1))
	def sub_url(self, match):
		s = ('<a target="_blank" style="text_decoration: none; color: #BC1A4B; href="{}">{}</a>')
		return s.format(match.group(1), match.group(1))
	def sub_mail(self, match):
		s = ('<a style="text_decoration: none; color: #BC1A4B; href="mailto:{}">{}</a>')
		return s.format(match.group(1), match.group(1))
	def feed(self, data):
		print(data)

if __name__ == '__main__':

	handler = Handler()
	# getattr 接收三个参数
	# 1、Python 对象
	# 2、属性字符串
	# 3、缺省值
	# 返回值为 Python 对象的属性值，如果没有此属性值，返回第三个参数
	# res1 = getattr(handler, 'start_test', None)
	# print(res1)
	# res2 = getattr(handler, 'test_getattr', None)
	# print(res2)
	# handler.start('test')

	html_rander = HTMLRenderer()
	html_rander.start('document')
	import re
	a = '我的qq：1245@qq.com'
	match = re.search(r'([\.a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z]+)', a)
	mail_html = html_rander.sub('mail')(match)
	print(mail_html)
	html_rander.end('document')