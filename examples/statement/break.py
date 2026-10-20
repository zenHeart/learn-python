l = [1,2,3,4]
i = 0

while i < len(l):
  if(l[i] > 2):
    print("first element greater 2 index: ", i)
    # break 跳出整个 while 循环，后面的迭代不再执行
    break;
  i+=1
