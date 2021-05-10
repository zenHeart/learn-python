def hi(self):
   print(f'hi {self.name}')
class C1:
   def __init__(self, name):
      self.name = name
   hi = hi


c1 = C1('tom')

# 1. 实例调用
c1.hi() # hi tom

# 2. 实例方法赋值给变量进行调用
g = c1.hi
g() # hi tom

# 3. 类调用
C1.hi(c1)

# 4. 类方法赋值给变量调用
h = C1.hi
h(c1) # hi tom

# 5. 函数调用
hi(c1) # hi tom