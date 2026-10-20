# 元素排序
items = ['A', 'tom', 'jerry', 'jack', '1']
items.sort()
# 按字符编码（码位）排序：数字 < 大写 < 小写。元素必须可互相比较，
# 混类型会抛 TypeError: '<' not supported between instances of 'str' and 'int'
print('list.sort():', items)

# sorted() 不改变原列表，返回排好序的新列表
items = ['A', 'tom', 'jerry', 'jack', '1']
print('sorted(list):', sorted(items), "list:", items)

# reverse 翻转 list 顺序（原地，返回 None）
items = ['A', 'tom', 'jerry', 'jack', '1']
items.reverse()
print('list.reverse():', items)
