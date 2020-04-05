# -*- coding: UTF-8 -*-
'''处理文本块的规则类，所有类均为单例模式，在程序运行时除了 Rule 每个类仅创建一个实例
'''


class Rule:
    """
    所有规则类的父类
    """

    def action(self, block, handler):
        """
        加标记，以下三行执行打印 HTML 标签的功能
        """
        handler.start(self.type)    # 打印标签头
        handler.feed(block)         # 打印标签 text 部分
        handler.end(self.type)      # 打印标签尾
        return True                 # 打印完成，返回 True


class HeadingRule(Rule):
    """
    一号标题规则，HTML 文件的一级标题规则（最大字号）<h1> 标签
    """

    type = 'heading'    # 文本块类型

    def condition(self, block):
        """
        判断文本块是否符合规则，返回值为布尔值 True 或 False
        """
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRule):
    """
    二号标题规则，次级标题规则，继承一号标题规则类 <h2> 标签
    """

    type = 'title'  # 文本块类型
    first = True    # 这是一个浮动值
                    # 首次调用该类的实例，该值为 True
                    # 之后调用该类的实例，该值为 False

    def condition(self, block):
        # 以下三行代码保证在首次调用该类实例和后续调用时 first 的值不同
        # 符合一号标题规则的文本块一定符合二号标题规则，它们只有先后次序这一个区别
        # 首次调用时返回 False ，即代码块不符合二号标题规则
        # 之后调用返回 True ，即使用该类的 action 方法进行处理
        if not self.first: 
            return False
        self.first = False
        return super().condition(block)


class ListItemRule(Rule):
    """
    列表项规则，<li> 标签
    """

    type = 'listitem'   # 文本块类型

    def condition(self, block):
        # 行首为减号，则该代码块符合列表项规则
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)        # 打印 <li> 标签头
        handler.feed(block[1:].strip()) # 打印 <li> 标签的 text 部分，注意去掉减号
        handler.end(self.type)          # 打印 <li> 标签尾
        return True                     # 处理完毕，返回 True


class ListRule(ListItemRule):
    """
    列表规则，<ul> 标签
    """
    type = 'list'   # 文本块类型
    inside = False  # 该值亦为浮动值，判断是否为列表规则

    def condition(self, block):
        # 判断代码块是否符合规则这里返回 True
        # 在 action 方法中调用父类的同名方法再次判断
        return True

    def action(self, block, handler):
        # 如果 self.inside 为 False 且父类的 condition 方法返回值为 True
        # 第一次出现符合列表项规则的文本块时，满足这两个要求
        if not self.inside and super().condition(block):
            # 打印 <ul> 标签头
            handler.start(self.type)
            # 将 inside 属性值改为 True
            self.inside = True
        # 打印一堆连续 li 标签后，出现非列表项规则的文本块
        elif self.inside and not super().condition(block):
            # 打印 <ul> 标签尾
            handler.end(self.type)
            # 再次修改 inside 属性为 False
            self.inside = False
        # 该方法只用于在合适的条件下打印 <ul> 标签
        # 永远返回 False ，以调用其它规则实例继续处理
        return False


class ParagraphRule(Rule):
    """
    段落规则，<p> 标签
    """

    type = 'paragraph'  # 文本块类型

    def condition(self, block):
        # 不符合以上各类的判断规则的代码块一律按此规则处理
        return True


# 注意这个列表中实例的顺序不能随意改动，原因参见相应类中的注释说明
rule_list = [ListRule(), ListItemRule(), TitleRule(), HeadingRule(),
        ParagraphRule()]