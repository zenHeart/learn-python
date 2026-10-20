# 删除列表元素
items = [1, True, 'tom', 1]
# 只删除第一次出现的值；remove 返回 None
remove = items.remove(1)
print("list:", items, "remove:", remove)

# 采用 del 删除元素
del items[0]
print("list:", items)

# 使用 pop 删除元素（无参时删最后一个）
items.pop()
print("list:", items)

# 支持传参弹出特定位置的值
items = [1, True, 'tom', 1]
# 返回弹出的值
pop = items.pop(2)
print("list:", items, "pop:", pop)
