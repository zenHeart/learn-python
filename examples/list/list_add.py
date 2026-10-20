# 访问列表元素的方法
items = [1, True, 'tom']
print("origin list:", items)

# 采用 append 修改原 list（原地修改，返回 None）
items.append('jack')
print("append list:", items)

# 采用 insert 方法
items = [1, True, 'tom']
items.insert(0, 'jack')
print("0 insert list:", items)

# 采用 + 操作符创建新 list,不会改变原 list 的值
new_list = items + ['tom']
print("new_list:", new_list)
print("list:", items)

# 采用 * 创建重复 list
print('[1]*5', [1]*5)
