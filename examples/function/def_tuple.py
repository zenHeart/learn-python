# 实现多个参数的传入
def show_name(*names):
    for name in names:
        print("name:", name)


show_name('tom', 'locke', 'jerry')
