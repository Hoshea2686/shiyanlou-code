# /urs/bin/python3
# -*-coding:utf-8-*-

# 需要将不同文本制定不同的规则， 做成一个规则列表， 
# 将block按顺序起去匹配这些规则的条件condition， 
# 如果满足就执行相应的action

class Rule:
	name = None
	def condtion(self, block):
		pass

	def action(self, block, handler):
		handler.start(self.name)
		handler.feed(block)
		handler.end(self.name)
		return True		# 返回True表示当前block处理完毕完毕

class HeadingRule(Rule):
	name = 'heading'
	def condition(self, block):
		return not '\n' in block and len(block)<=70 and block[-1] != ':'

class TitleRule(HeadingRule):
	# 大标题同时也满足二级标题的条件（继承）， 但是大标题只有一个 。
	name = 'title'
	first = True   # 控制满足条件的次数有且只有第一1次

	def condition(self, block):
		if not self.first:
			return False
		self.first = False
		return super().condition(block)

class ListItemRule(Rule):
	name = 'listitem'

	def condition(self, block):
		return block[0] == '-'

	def action(self, block, handler):
		handler.start(self.name)
		handler.feed(block[1:])
		handler.end(self.name)
		return True

class ListRule(ListItemRule):
	"""
	<ul>
		<li></li>
		<li></li>
	</ul>
	"""
	
	# <ul>标签：在第一个<li>前加<ul>;在最后一个</li>后加</ul>
	# <ul>共享了第一个<li>和最后一个<li>的block

	name = 'list'
	inside = False

	# 比较特殊，先假设满足条件。在action中再判断
	def condition(self, block):
		return True

	def action(self, block, handler):
		if not self.inside and super().condition(block):
			handler.start(self.name)
			self.inside = True
		if self.inside and not super().condition(block):
			handler.end(self.name)
			self.inside = False
		return False

class ParagraphRule(Rule):
	"""
	段落规则，<p> 标签
	"""

	name = 'paragraph'  # 文本块类型

	def condition(self, block):
		# 不符合以上各类的判断规则的代码块一律按此规则处理
		return True

rule_list = [ListRule(), ListItemRule(), TitleRule(), HeadingRule(), ParagraphRule()]
