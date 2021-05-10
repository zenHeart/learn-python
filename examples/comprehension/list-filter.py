a = list(range(1,15))
def double(el):
   return el*2

def is_even(el):
   return el%2 == 0;


double_even_in_a= [ double(el) for el in a if  is_even(el)]

print(double_even_in_a) # [4, 8, 12, 16, 20, 24, 28]