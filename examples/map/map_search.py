# 采用花括号初始化字典
profile = {'name': 'tom', 'age': 12}

# 采用键名索引字典
print('map["name"]:', profile['name'])

# 采用 items 返回 (键, 值) 元组的视图，可直接循环解包
print("map.items():", profile.items())
for key, value in profile.items():
    print("key:", key, "value:", value)

# 采用 keys 遍历所有键
print("map.keys():", profile.keys())
for key in profile.keys():
    print("key:", key)

# 采用 values 遍历所有值
print("map.values():", profile.values())
for value in profile.values():
    print("value:", value)
