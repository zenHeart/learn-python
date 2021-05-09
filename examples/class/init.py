class Person:
   def __init__(self, name,age):
      # 初始化实例对象的属性
      self.name = name
      self.age = age
   def eat(self):
      print(f"{self.name} eat")

# 实例化 person 创建 tom 的信息
tom = Person('tom', 10)
print(f"{tom.name}, age:{tom.age}") # tom, age: 10
tom.eat() # tom eat

# 实例化 person 创建 jack 的信息
jack = Person('jack', 3)
print(f"{jack.name}, age:{jack.age}") # jack, age: 3
jack.eat() # jack eat
