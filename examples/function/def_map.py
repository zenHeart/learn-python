# 实现 map 数组传入
def user_profile(name, age, **info):
    user = {'name': name, 'age': age}
    for key, value in info.items():
        user[key] = value
    return user

user = user_profile(name='tom', age=10, city='berlin', sex='man')
print(user)
