# use blackslash split logic line to multi physical line
n = int(input("please enter a number: "));

if  n > 10 \
  and n % 2 == 0 :
    print("n is bigger than 10 even number")
else: 
    print("not illegal number")



# use [], {}, () can explicit line join
list = [ 
          1, 2, 3,
          4, 5, 6,
          7, 8, 9 ]
print(list)