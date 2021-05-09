# 浮点数
print(1.1 + 1.2) # 1.3
print(-0.23) # -0.23


# 科学计数法 
print(1e5) # 100000
print(1.1e-2) # 0.011
print(1.22e3) # 1220.0

# 复数运算
print(1j + 1j) # 2j
print(1j - 1j) # 0j
print(1j * 1j) # -1 + 0j
print(1j / 1j) # 1 + 0j


# 0b,0B 表示 二进制表示
print(0b10, 0B1011) # 2 11
# 0o,0O 表示八进制表示
print(0o1, 0O1) # 1 1
# 0x,0X 表示 十六进制
print(0x1, 0x1) # 1 1

# 采用 _ 分隔数据
print(1_000_000) # 1000000
# 支持其他进制
print(0b0000_1000) # 8
print(0o000_100) # 64
print(0x00_ff) # 255