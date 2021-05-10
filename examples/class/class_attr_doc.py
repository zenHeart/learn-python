class C:
   """类注释
   示例类 C

   test
   """
   def hi():
      print('hi')

# 类上访问
print(C.__doc__)

# 实例上访问
c1 = C()
print(c1.__doc__)

