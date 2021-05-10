import os

# path 连接目录
print(os.path.join('/a' , 'b' , 'c'))

# 获取当前路径
print(os.getcwd()) # 使用数据
print(os.path.abspath('./a')) # 返回 pwd + 当前路径

# 判断是否为绝对路径
print(os.path.isabs('/a/b/c')) # True
print(os.path.isabs('./a')) # False
