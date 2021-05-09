# formatted string literals https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals, support in python in 3.7
# 1. use { } to replace variable
a = 'hello'
print(f"{a} world")

# 2. support multi {} replace more than one variable
a,b = 'hello','world'
print(f"{a} {b}")

# 3. 
