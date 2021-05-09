# 携带返回值的函数
def fullname(firstname, middlename, lastname):
    fullname = firstname + ' ' + middlename+' ' + lastname
    return fullname.title()

print(fullname('tom', 'lee', 'hooker'))
