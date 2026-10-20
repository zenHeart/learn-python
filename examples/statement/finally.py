try:
    x = int(input("Please enter a number: "))
    print('x is a valid number:', x)
# 只捕获 ValueError，不用裸 except:（会连 KeyboardInterrupt 一起吞掉）
except ValueError:
    print("Oops! That was not a valid number.")
finally:
    print("over")
