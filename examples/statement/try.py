try:
    x = int(input("Please enter a number: "))
    print('x is a valid number:', x)
# 只捕获 ValueError：裸 except: 会把 KeyboardInterrupt、SystemExit 一起吞掉，
# 导致 Ctrl+C 停不下程序。
except ValueError:
    print("Oops! That was not a valid number.")