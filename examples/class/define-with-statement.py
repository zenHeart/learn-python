class C1:
   # 这些语句会在文件执行时触发
   print("test")
   for i in range(1,10):
      print(i)
   if __module__ == '__main__':
      print('main')      