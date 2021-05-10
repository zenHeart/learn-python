class C:
   """类注释
   示例类 C

   test
   """
   def hi():
      print('hi')

print(C.__class__ == C) # False

c1 = C()
print(c1.__class__ == C) # True

