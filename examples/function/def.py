# 斐波那契函数
def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()


n = int(input("enter a number:"))
fib(n)
