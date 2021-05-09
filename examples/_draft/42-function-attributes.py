# special varibale
# __doc__ function documention variable
def hi():
    """ 
    demo function hi
    this is a test comment
    """
    print("hi")
print(hi.__doc__)
# you can change __doc__ data
hi.__doc__ = 'change comment'
print(hi.__doc__)

# special varibale
# __name__ function name variable
def say(tom = 'tom'):
    b = 1
    print("say")
    return lambda a: a + b
print(say.__name__)
# you can change __name__ data
say.__name__ =  'hi1'
print(say.__name__, say.__qualname__)
# __defaults__， tuple save function default values
print(say.__defaults__)
print(say.__code__)

print(hi.__globals__)
say.a = {'a' : 1}
print(say.__dict__)
print(say.__closure__)
print(say.__annotations__)
print(say.__kwdefaults__)
