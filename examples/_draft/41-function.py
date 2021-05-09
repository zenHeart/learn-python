def make_incrementor(n):
    return lambda x: x + n

f1 = make_incrementor(1)

print(f1(0))
print(f1(1))
print(f1(2))
