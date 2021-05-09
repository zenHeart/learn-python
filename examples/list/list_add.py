# 访问列表元素的方法
list = [1, True, 'tom']
print("origin list:", list)

# 采用 append 修改原list
list.append('jack')
print("append list:", list)

# 采用 insert 方法
list = [1, True, 'tom']
list.insert(0, 'jack')
print(" 0 insert list:", list)

# 采用 + 操作符创建新 list,不会改变原 list 的值
new_list = list+['tom']
print("new_list:", new_list)
print("list:", list)

# 采用 * 创建重复 list
print('[1]*5', [1]*5)
