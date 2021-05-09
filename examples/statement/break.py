l = [1,2,3,4]
i = 0

while i < len(l):
  if(l[i] > 2):
    print("first element greater 2 index: ", i)
    # jump to loop
    break;
  i+=1
