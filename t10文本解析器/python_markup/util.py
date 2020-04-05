# -*- coding: UTF-8 -*-
'''处理 TXT 文本，创建返回文本块的生成器'''


# 生成器函数，函数调用为生成器
# 调用此函数时，file 参数一定是 IOWrapper 对象，IOWrapper 对象是迭代器对象
# 该函数的作用是给文本文件的 IOWrapper 迭代器的末尾增加一个换行符
def lines(file):
    """生成器，在文本最后加一空行
    """
    for line in file: 
        yield line
    yield '\n'


# 同上一个函数 lines ，它也是个生成器函数
# 调用此函数时，file 参数一定是 IOWrapper 对象，IOWrapper 对象是迭代器对象 
# 函数的返回值是生成器，生成器的每次迭代都会返回一个文本块
def blocks(file):
    """生成器，将 TXT 文件内容生成一个个单独的文本块，按空行分
    """
    block = []
    # 使用 for 循环调用生成器
    for line in lines(file):
        # 如果不是空行
        if line.strip():
            # 将该行数据添加到 block 列表里
            block.append(line)
        # 如果是空行，且 block 列表里有内容
        # 这里可以看出 lines 生成器函数的作用了，如果最后一行不是空行
        # 那么最后一个文本块就不会作为 yield 的参数被生成器返回
        elif block:
            yield ''.join(block).strip()
            # 每次生成文本块后，要清空 block 列表
            block = []

