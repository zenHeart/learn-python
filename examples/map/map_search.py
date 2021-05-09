# 采用方括号初始化列表
map = {'name': 'tom', 'age': 12}

# 采用键名索引 map
print('map["name"]:', map['name'])

# 采用 in 遍历字典
# 采用 items 返回二维数组模式
print("map.items():", map.items())
for key, value in map.items():
    print("key:", key, "value:", value)

# 采用 keys 遍历所有键
print("map.keys():", map.keys())
for key in map.keys():
    print("key:", key)

# 采用 values 遍历所有值
print("map.values():", map.values())
for value in map.values():
    print("value:", value)
