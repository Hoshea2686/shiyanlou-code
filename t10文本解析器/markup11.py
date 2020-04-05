# /urs/bin/python3
# -*-coding:utf-8-*-

import sys, re
from handlers11 import HTMLRenderer
from util11 import blocks
from rules import rule_list

class Parser(object):
	"""docstring for ClassName"""
	def __init__(self, handler):
		self.handler = handler
		self.rules = []
		self.filters = []

	def addRule(self, rule):
		self.rules.append(rule)

	def addFilter(self, pattern, name):
		"""
		pattern:为正则表达式
		name：为前面定义的HTML渲染的函数
		"""
		def filter(block, handler):
			return re.sub(pattern, handler.sub(name), block)

		self.filters.append(filter)

    def parse(self, file):
        """
        核心方法，解析文本，打印符合要求的标签，写入新的文件中
        """
        # 调用 handler 实例的 start 方法，参数为 handler 实例的某个方法名的一部分
        # 结果就是调用 handler 的 start_document 方法，打印文档的 head 标签
        self.handler.start('document')
        # blocks 是从 urti.py 文件引入的生成器函数
        # blocks(file) 就是一个生成器
        # 使用 for 循环生成器
        for block in blocks(file):
            # 调用过滤器，对每个文本块进行处理
            for filter in self.filters:
                block = filter(block, self.handler)
            # 循环规则类的实例
            for rule in self.rules:
                # 如果符合规则，调用实例的 action 方法打印标签
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    # 如果 action 方法的返回值为 True
                    # 表示该文本块处理完毕，结束循环
                    if last:
                        break
        # 同 self.handler.start
        # 调用 handler 的 end_document 方法打印 '</body></html>'
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    纯文本解析器
    """

    def __init__(self, handler):
        # 运行父类 Parser 的同名方法
        super().__init__(handler)
        # 增加规则类的实例到 self.urls 列表
        for rule in rule_list:
            self.addRule(rule)
        # 增加三个过滤函数，分别处理斜体字段、链接和邮箱
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


def main():
    '''
    主函数，控制整个程序的运行
    '''
    handler = HTMLRenderer()
    parser = BasicTextParser(handler)
    # 将文件内容作为标准输入，sys.stdin 获取标准输入的内容，生成 IOWrapper 迭代器对象
    parser.parse(sys.stdin)


if __name__ == '__main__':
    main()