class Person:
   type = 'person'
   def __init__(self, name,age):
      # 初始化实例对象的属性
      self.name = name
      self.age = age
   def eat(self):
      print(f"{self.name} eat")

# 可以直接在类上引用该属性
print(Person.type) # person

# 实例化 person 创建 tom 的信息
tom = Person('tom', 10)
# 也可直接在实例上访问类属性
print(tom.type) # person
tom.eat() # tom eat

# 实例化 person 创建 jack 的信息
jack = Person('jack', 3)
# 也可直接在实例上访问类属性
print(jack.type) # person
jack.eat() # jack eat

