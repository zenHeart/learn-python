# 访问列表元素的方法
items = [1, True, 'tom']

# 第一个元素
print('list[0]:', items[0])
# 最后一个元素
print('list[len(list) - 1]:', items[len(items) - 1])
print('list[-1]:', items[-1])

# 切片访问局部元素
#  0,1 ,注意前面是闭区间后面为开区间
print('list[0:2]:', items[0:2])

# 访问 1,2
print('list[1:]:', items[1:])
print('list[-2:]:', items[-2:])
