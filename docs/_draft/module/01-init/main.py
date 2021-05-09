# import all
import math
print(math.add(1 ,2))
print(math.minus(2 ,1))

# import by name
from math import add, minus
print(add(1,2))
print(minus(2, 1))

# import with another name
import math as math1
print(math1.add(1 ,2))
print(math1.minus(2 ,1))

# import with another name
from math import add as add1, minus as minus1
print(add1(1,2))
print(minus1(2, 1))

