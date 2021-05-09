# 元素排序
list = ['A', 'tom', 'jerry', 'jack', '1']
list.sort()
# 字典排序,注意 list 必须为同一类型否则会报错
print('list.sort():', list)

# sorted 不该边原始排序
list = ['A', 'tom', 'jerry', 'jack', '1']
print('sorted(list):', sorted(list), "list:", list)

# reverse 翻转 list 顺序
list = ['A', 'tom', 'jerry', 'jack', '1']
list.reverse()
print('list.reverse():', list)
