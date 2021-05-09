# 删除列表元素
list = [1, True, 'tom', 1]
# 只删除第一次出现的值
remove = list.remove(1)
print("list:", list, "remove:", remove)

# 采用 del 删除元素
del list[0]
print("list:", list)

# 使用 pop 删除元素
list.pop()
print("list:", list)

# 支持传参弹出特定位置的值
list = [1, True, 'tom', 1]
# 返回弹出的值
pop = list.pop(2)
print("list:", list, "pop:", pop)
