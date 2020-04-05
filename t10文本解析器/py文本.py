# /urs/bin/python3
# -*-coding:utf-8-*-

import sys


print('测试重定向输入，将终端中的 < 后的文件作为参数赋值给py代码中sys.stdin', sys.stdin)
print('测试重定向输出，程序运行时 print 方法打印到终端的内容重定向(>)到文件 test.txt 中')


# < 为重定向命令符，将 test.txt 文件内容作为标准输入
# > 也是重定向命令符，将标准输出（即程序运行时 print 方法打印到终端的内容）重定向到文件 test.txt 中

# 例1：
# 在终端中输入 
# python3 py文本.py < test.txt > test.txt
# 会将输出结果保存在test.txt文件中
