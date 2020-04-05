# /urs/bin/python3
# -*-coding:utf-8-*-

class Handler:
	def callback(self, prefix, name, *args):
		"""
		调用自己的方法
		"""
		method = getattr(self, prefix+name, None)
		if callable(method):
			return method(*args)
	def start(self, name):
		self.callback('start_', name)

	def end(self, name):
		self.callable('end_', name)
	def sub(self, name):
		# name 为过滤器名字，
		def substitution(match):
			result = self.callback('sub_', name, match)
			if result is None: # 如果没有这个过滤器
				result = match.group(0) # 获取match中所有内容
			return result
		return substitution

class HTMLRenderer(Handler):
	"""
    HTML 处理程序，给文本块加相应的 HTML 标记
    """

    # 以下各个方法分别在符合条件时被调用，打印标签或标签的 text 值

    def start_document(self):
        print('<html><head><title>ShiYanLou</title></head><body>')

    def end_document(self):
        print('</body></html>')

    def start_paragraph(self):
        print('<p style="color: #444;">')

    def end_paragraph(self):
        print('</p>')

    def start_heading(self):
        print('<h2 style="color: #68BE5D;">')

    def end_heading(self):
        print('</h2>')

    def start_list(self):
        print('<ul style="color: #363736;">')

    def end_list(self):
        print('</ul>')

    def start_listitem(self):
        print('<li>')

    def end_listitem(self):
        print('</li>')

    def start_title(self):
        print('<h1 style="color: #1ABC9C;">')

    def end_title(self):
        print('</h1>')

    def sub_emphasis(self, match):
        return('<em>%s</em>' % match.group(1))

    def sub_url(self, match):
        s = ('<a target="_blank" style="text-decoration: none;'
                'color: #BC1A4B;" href="{}">{}</a>')
        return s.format(match.group(1), match.group(1))
    
    # 邮箱过滤器
    # 当通过正则表达式比配到了邮箱的时候，将匹配到的文本作为参数传递过来， 用match接受该参数，
    def sub_mail(self, match):
        s = ('<a style="text-decoration: none;color: #BC1A4B;" '
                'href="mailto:{}">{}</a>')
        return s.format(match.group(1), match.group(1))

    def feed(self, data):
        print(data)
