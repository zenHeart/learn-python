# extract string 
a = 'python'
print(a[0:2])  # py
print(a[-2:-1])  # o

print(a[0:])  # python
print(a[:-1])  # pytho

# 不报错，返回空
print(a[7:9])
# 范围包含整个字符，取所有字符
print(a[-10:9]) # python