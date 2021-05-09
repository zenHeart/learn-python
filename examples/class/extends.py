class Person:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("run ", self.name)


class Student(Person):
    def __init__(self, name, school):
        super().__init__(name)
        self.school = school

    def learn(self):
        print('learn')


tom = Student('tom', 's1')
print('tom.name:', tom.name)
print('tom.school:', tom.school)
tom.learn()
