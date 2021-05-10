class C1:
   def __init__(self, name):
      self.name = name
   def hi(self):
      print(f'hi {self.name}')

c1 = C1('tom')
c1.hi() # hi tom
# 也可直接采用类的方式调用
C1.hi(c1) # hi tom 