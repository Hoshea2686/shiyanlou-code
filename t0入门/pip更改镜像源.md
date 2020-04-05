# Linux下更换镜像源

修改 `~/.pip/pip.conf` 文件, 没有则创建

	mkdir ~/.pip
	vim ~/.pip/pip.conf

修改内容为：
	[global]
	timeout = 6000
	index-url = https://pypi.tuna.tsinghua.edu.cn/simple
	trusted-host = pypi.tuna.tsinghua.edu.cn

更新pip3:

	pip3 install --upgrade pip


