class C:
   type = 'C'
   def __init__(self, foo):
      self.type = foo

# 可以直接在类上引用该属性
print(C.type) # C

c1 = C('c1')
# 实例属性覆盖类同名属性
print(c1.type) # c1

c2 = C('c2')
# 实例属性覆盖类同名属性
print(c2.type) # c2


