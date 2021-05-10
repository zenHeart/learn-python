class C1:
   def __init__(self, name):
      self.name = name
   def hi(self):
      print(f'hi {self.name}')

c1 = C1('tom')
g = c1.hi
g() # hi tom

h = C1.hi
h(c1) # hi tom