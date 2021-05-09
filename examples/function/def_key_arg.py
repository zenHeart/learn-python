# 验证关键字实参的调用
def hi(time, name):
    print(time+" " + name)


hi(time='morning', name="tom")
# 直接指明形参名则无需考虑传入顺序
hi(name='tom', time="morning")
