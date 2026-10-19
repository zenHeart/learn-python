try:
  a = 1 / 0
except ZeroDivisionError:
  print("除零被捕获")
else:
  print("没有异常时走这里")
finally:
  print("finally 总会执行")

# for-else：循环完整跑完（没遇到 break）才执行 else
for i in range(3):
  print("i =", i)
else:
  print("循环正常结束，未被 break 打断")

for i in range(3):
  if i == 1:
    break
  print("i =", i)
else:
  print("这一行不会执行，因为上面 break 了")
