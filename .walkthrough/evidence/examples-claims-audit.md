C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\.walkthrough\evidence\examples-claims-audit.py:777: SyntaxWarning: "is" with a literal. Did you mean "=="?
  check("L7 反例: 1 == True 但 1 is True 为 False", (True, False), (1 == True, 1 is True))
========================================================================
A. examples/number/ —— 3 个文件
========================================================================
[PASS] A1 converter.py: print(1.1 + 1.2) 注释写 # 1.3，实际是 2.3
       示例声称: '2.3'
       实际得到: '2.3'
[PASS] A2 converter.py: 1.1 + 1.2 的值本身等于 2.3
       示例声称: 2.3
       实际得到: 2.3
[PASS] A3 converter.py: print(1e5) 注释写 # 100000，实际带 .0
       示例声称: '100000.0'
       实际得到: '100000.0'
[PASS] A4 converter.py: 1e5 的类型是 float 不是 int
       示例声称: 'float'
       实际得到: 'float'
[PASS] A5 converter.py: print(1.1e-2)
       示例声称: '0.011'
       实际得到: '0.011'
[PASS] A6 converter.py: print(1.22e3)
       示例声称: '1220.0'
       实际得到: '1220.0'
[PASS] A7 converter.py: 1j + 1j
       示例声称: '2j'
       实际得到: '2j'
[PASS] A8 converter.py: 1j - 1j
       示例声称: '0j'
       实际得到: '0j'
[PASS] A9 converter.py: 1j * 1j（虚数单位自乘得 -1）
       示例声称: '(-1+0j)'
       实际得到: '(-1+0j)'
[PASS] A10 converter.py: 1j / 1j
       示例声称: '(1+0j)'
       实际得到: '(1+0j)'
[PASS] A11 converter.py: 0b10, 0B1011
       示例声称: '2 11'
       实际得到: '2 11'
[PASS] A12 converter.py: 0o1, 0O1
       示例声称: '1 1'
       实际得到: '1 1'
[PASS] A13 converter.py: 0x1, 0x1
       示例声称: '1 1'
       实际得到: '1 1'
[PASS] A14 converter.py: 1_000_000 下划线分隔
       示例声称: 1000000
       实际得到: 1000000
[PASS] A15 converter.py: 0b0000_1000
       示例声称: 8
       实际得到: 8
[PASS] A16 converter.py: 0o000_100
       示例声称: 64
       实际得到: 64
[PASS] A17 converter.py: 0x00_ff
       示例声称: 255
       实际得到: 255
[PASS] A18 float.py: 0.1+0.1+0.1 == 0.3 为 False
       示例声称: False
       实际得到: False
[PASS] A19 float.py: 0.1+0.1+0.1 的真实 repr
       示例声称: '0.30000000000000004'
       实际得到: '0.30000000000000004'
[PASS] A20 float.py: 0.1+0.2 同样不精确
       示例声称: '0.30000000000000004'
       实际得到: '0.30000000000000004'
[PASS] A21 float.py: round(..., 2) 可以把显示救回 0.3
       示例声称: True
       实际得到: True
[PASS] A22 operator.py: 2 + 2
       示例声称: 4
       实际得到: 4
[PASS] A23 operator.py: 2 - 2
       示例声称: 0
       实际得到: 0
[PASS] A24 operator.py: 2 * 3
       示例声称: 6
       实际得到: 6
[PASS] A25 operator.py: 2 / 3（/ 永远得 float）
       示例声称: '0.6666666666666666'
       实际得到: '0.6666666666666666'
[PASS] A26 operator.py: 2 // 3 向下取整
       示例声称: 0
       实际得到: 0
[PASS] A27 operator.py: 2 ** 3
       示例声称: 8
       实际得到: 8
[PASS] A28 operator.py: 5 - 1 * 4（乘法优先）
       示例声称: 1
       实际得到: 1
[PASS] A29 operator.py: (5 - 1) * 4（括号优先）
       示例声称: 16
       实际得到: 16
[PASS] A30 反例: -7 // 2 是 -4 不是 -3（向负无穷取整）
       示例声称: -4
       实际得到: -4
[PASS] A31 反例: -7 % 2 是 1 不是 -1（余数符号跟随除数）
       示例声称: 1
       实际得到: 1
[PASS] A32 反例: divmod(7, -2) = (-4, -1)
       示例声称: (-4, -1)
       实际得到: (-4, -1)
[PASS] A33 反例: 17.0 // 3 得 5.0，整除不保证是 int
       示例声称: '5.0'
       实际得到: '5.0'
[PASS] A34 反例: 2 ** -1 得 0.5，幂运算支持负指数
       示例声称: 0.5
       实际得到: 0.5
[PASS] A35 反例: 2 ** 0.5 得无理数近似
       示例声称: 1.4142135623730951
       实际得到: 1.4142135623730951

========================================================================
B. examples/string/ —— 7 个文件
========================================================================
[PASS] B1 escape.py: 'test\nbreak line' 长度 15
       示例声称: 15
       实际得到: 15
[PASS] B2 escape.py: "hello\tworld!" 长度 12
       示例声称: 12
       实际得到: 12
[PASS] B3 escape.py: print('\\') 输出单字符反斜杠
       示例声称: '\\'
       实际得到: '\\'
[PASS] B4 escape.py: len('\\') == 1
       示例声称: 1
       实际得到: 1
[PASS] B5 escape.py: len('a\nb') == 3（转义后只算 1 个字符）
       示例声称: 3
       实际得到: 3
[PASS] B6 escape-r.py: r'test\nbreak line' 长度 16（\n 是两个字符）
       示例声称: 16
       实际得到: 16
[PASS] B7 escape-r.py: r'hello\tworld!' 含字面反斜杠+t
       示例声称: True
       实际得到: True
[PASS] B8 escape-r.py: r'\\' 是两个字符
       示例声称: 2
       实际得到: 2
[PASS] B9 反例: r-string 不能以奇数个反斜杠结尾
       预期异常: SyntaxError
       实际得到: SyntaxError: unterminated string literal (detected at line 1) (<s>, line 1)
[PASS] B10 index.py: 'python'[0]
       示例声称: 'p'
       实际得到: 'p'
[PASS] B11 index.py: 'python'[-1]
       示例声称: 'n'
       实际得到: 'n'
[PASS] B12 index.py: 用变量索引 a[0] 同样得 'p'
       示例声称: 'p'
       实际得到: 'p'
[PASS] B13 反例: 'python'[6] 越界抛 IndexError（下标不做裁剪）
       预期异常: IndexError
       实际得到: IndexError: string index out of range
[PASS] B14 len.py: len('banana')
       示例声称: 6
       实际得到: 6
[PASS] B15 operator.py: 'ba' + 'na'*2 —— * 优先于 +
       示例声称: 'banana'
       实际得到: 'banana'
[PASS] B16 operator.py: 'ba' + 'na' + 'na'
       示例声称: 'banana'
       实际得到: 'banana'
[PASS] B17 operator.py: 相邻字符串字面量自动拼接
       示例声称: 'banana'
       实际得到: 'banana'
[PASS] B18 operator.py: 单双引号混写也拼
       示例声称: 'banana'
       实际得到: 'banana'
[PASS] B19 反例: 'a' + 1 抛 TypeError（str 不与 int 相加）
       预期异常: TypeError
       实际得到: TypeError: can only concatenate str (not "int") to str
[PASS] B20 反例: '10' + '20' 是 '1020' 不是 30
       示例声称: '1020'
       实际得到: '1020'
[PASS] B21 反例: int('10') + int('20') 才是 30
       示例声称: 30
       实际得到: 30
[PASS] B22 quote.py: 单双引号打印结果一致
       示例声称: ('hello world!', 'hello world!')
       实际得到: ('hello world!', 'hello world!')
[PASS] B23 quote.py: 注释写作带反斜杠的 '"Isn\'t," ...'，真实输出不含反斜杠
       示例声称: '"Isn\'t," they said.'
       实际得到: '"Isn\'t," they said.'
[PASS] B24 quote.py: 该字符串长度 19
       示例声称: 19
       实际得到: 19
[PASS] B25 反例: 单引号字符串不能跨行（跨行要用三引号）
       预期异常: SyntaxError
       实际得到: SyntaxError: unterminated string literal (detected at line 1) (<s>, line 1)
[PASS] B26 slice.py: a[0:2]
       示例声称: 'py'
       实际得到: 'py'
[PASS] B27 slice.py: a[-2:-1]
       示例声称: 'o'
       实际得到: 'o'
[PASS] B28 slice.py: a[0:]
       示例声称: 'python'
       实际得到: 'python'
[PASS] B29 slice.py: a[:-1]
       示例声称: 'pytho'
       实际得到: 'pytho'
[PASS] B30 slice.py: a[7:9] 越界切片返回空串、不报错
       示例声称: ''
       实际得到: ''
[PASS] B31 slice.py: a[-10:9] 负越界被裁剪成整串
       示例声称: 'python'
       实际得到: 'python'
[PASS] B32 反例: a[::2] 步长 2
       示例声称: 'pto'
       实际得到: 'pto'
[PASS] B33 反例: a[::-1] 负步长即反转
       示例声称: 'nohtyp'
       实际得到: 'nohtyp'
[PASS] B34 反例: 切片前闭后开，a[0:2] 长度是 2 不是 3
       示例声称: 2
       实际得到: 2
[PASS] B35 string-literal.py: 三引号 + 行首 \ 得到 3 行且首行无空行
       示例声称: 'Usage: thingy [OPTIONS]\n     -h                        Display this usage message\n     -H hostname               Hostname to connect to\n'
       实际得到: 'Usage: thingy [OPTIONS]\n     -h                        Display this usage message\n     -H hostname               Hostname to connect to\n'

========================================================================
C. examples/list/ —— 7 个文件
========================================================================
[PASS] C1 list_init.py: [1, True, 'tom'] 三种类型可混放
       示例声称: [1, True, 'tom']
       实际得到: [1, True, 'tom']
[PASS] C2 list_init.py: for item in list 顺序即插入顺序
       示例声称: ['1', 'True', 'tom']
       实际得到: ['1', 'True', 'tom']
[PASS] C3 list_modify.py: list[1] = False
       示例声称: [1, False, 'tom']
       实际得到: [1, False, 'tom']
[PASS] C4 list_add.py: append 是原地修改
       示例声称: [1, True, 'tom', 'jack']
       实际得到: [1, True, 'tom', 'jack']
[PASS] C5 list_add.py: append 返回 None（不能链式写）
       示例声称: None
       实际得到: None
[PASS] C6 list_add.py: insert(0, 'jack') 插到头部
       示例声称: ['jack', 1, True, 'tom']
       实际得到: ['jack', 1, True, 'tom']
[PASS] C7 list_add.py: + 生成新列表，原列表不变
       示例声称: [1, True, 'tom']
       实际得到: [1, True, 'tom']
[PASS] C8 list_add.py: [1] * 5
       示例声称: [1, 1, 1, 1, 1]
       实际得到: [1, 1, 1, 1, 1]
[PASS] C9 反例: [[]] * 3 的三个元素是同一个对象
       示例声称: True
       实际得到: True
[PASS] C10 反例: 所以 x[0].append(1) 会改掉三个
       示例声称: [[1], [1], [1]]
       实际得到: [[1], [1], [1]]
[PASS] C11 list_del.py: remove(1) 只删第一次出现，返回 None
       示例声称: ([True, 'tom', 1], None)
       实际得到: ([True, 'tom', 1], None)
[PASS] C12 反例: remove 不存在的值抛 ValueError
       预期异常: ValueError
       实际得到: ValueError: list.remove(x): x not in list
[PASS] C13 list_del.py: del list[0] 后剩 ['tom', 1]
       示例声称: ['tom', 1]
       实际得到: ['tom', 1]
[PASS] C14 list_del.py: pop() 返回并删除末元素
       示例声称: ('1', ['tom'])
       实际得到: ('1', ['tom'])
[PASS] C15 list_del.py: pop(2) 返回指定位置的值 'tom'
       示例声称: ('tom', [1, True, 1])
       实际得到: ('tom', [1, True, 1])
[PASS] C16 list_del.py: 对空列表 pop 抛 IndexError
       预期异常: IndexError
       实际得到: IndexError: pop from empty list
[PASS] C17 list_order.py: sort() 按码位排序，数字<大写<小写
       示例声称: ['1', 'A', 'jack', 'jerry', 'tom']
       实际得到: ['1', 'A', 'jack', 'jerry', 'tom']
[PASS] C18 list_order.py: '1'(49) < 'A'(65) < 'a'(97) < 'j'(106)
       示例声称: [49, 65, 97, 106]
       实际得到: [49, 65, 97, 106]
[PASS] C19 list_order.py: sort() 原地排序且返回 None
       示例声称: None
       实际得到: None
[PASS] C20 list_order.py: sorted() 返回新列表，原列表不动
       示例声称: (['1', 'A', 'jack', 'jerry', 'tom'], ['A', 'tom', 'jerry', 'jack', '1'])
       实际得到: (['1', 'A', 'jack', 'jerry', 'tom'], ['A', 'tom', 'jerry', 'jack', '1'])
[PASS] C21 list_order.py: reverse() 原地翻转且返回 None
       示例声称: None
       实际得到: None
[PASS] C22 反例: 混类型 sort 抛 TypeError（注释声称「必须同一类型」）
       预期异常: TypeError
       实际得到: TypeError: '<' not supported between instances of 'str' and 'int'
[PASS] C23 反例: sorted 混类型同样抛 TypeError
       预期异常: TypeError
       实际得到: TypeError: '<' not supported between instances of 'str' and 'int'
[PASS] C24 list_search.py: list[0]
       示例声称: 1
       实际得到: 1
[PASS] C25 list_search.py: list[len(list)-1]
       示例声称: 'tom'
       实际得到: 'tom'
[PASS] C26 list_search.py: list[-1] 与上一行等价
       示例声称: 'tom'
       实际得到: 'tom'
[PASS] C27 list_search.py: list[0:2] 前闭后开
       示例声称: [1, True]
       实际得到: [1, True]
[PASS] C28 list_search.py: list[1:]
       示例声称: [True, 'tom']
       实际得到: [True, 'tom']
[PASS] C29 list_search.py: list[-2:] 与 list[1:] 等价
       示例声称: [True, 'tom']
       实际得到: [True, 'tom']
[PASS] C30 反例: 用 in 判断成员比手写下标循环直接
       示例声称: True
       实际得到: True
[PASS] C31 反例: index() 找不到抛 ValueError
       预期异常: ValueError
       实际得到: ValueError: 9 is not in list

========================================================================
D. examples/map/ —— 5 个文件
========================================================================
[PASS] D1 map_init.py: {'name': 'tom', 'age': 12}
       示例声称: {'name': 'tom', 'age': 12}
       实际得到: {'name': 'tom', 'age': 12}
[PASS] D2 map_init.py: 键名可以是变量表达式
       示例声称: {'name': 'tom', 'age': 12}
       实际得到: {'name': 'tom', 'age': 12}
[PASS] D3 map_init.py: 键的顺序 = 插入顺序（3.7+）
       示例声称: ['name', 'age']
       实际得到: ['name', 'age']
[PASS] D4 反例: 重复键后者覆盖前者
       示例声称: {'a': 2}
       实际得到: {'a': 2}
[PASS] D5 map_add.py: 直接赋新键即新增
       示例声称: {'name': 'tom', 'age': 12, 'birth': 2000}
       实际得到: {'name': 'tom', 'age': 12, 'birth': 2000}
[PASS] D6 map_del.py: del map['name']
       示例声称: {'age': 12}
       实际得到: {'age': 12}
[PASS] D7 map_modify.py: map['age'] = 20
       示例声称: {'name': 'tom', 'age': 20}
       实际得到: {'name': 'tom', 'age': 20}
[PASS] D8 map_search.py: map['name']
       示例声称: 'tom'
       实际得到: 'tom'
[PASS] D9 map_search.py: items() 返回 (键, 值) 元组的视图
       示例声称: [('name', 'tom'), ('age', 12)]
       实际得到: [('name', 'tom'), ('age', 12)]
[PASS] D10 map_search.py: items() 的类型名是 dict_items
       示例声称: 'dict_items'
       实际得到: 'dict_items'
[PASS] D11 map_search.py: keys()
       示例声称: ['name', 'age']
       实际得到: ['name', 'age']
[PASS] D12 map_search.py: values()
       示例声称: ['tom', 12]
       实际得到: ['tom', 12]
[PASS] D13 map_search.py: for key, value in map.items() 循环解包
       示例声称: [('name', 'tom'), ('age', 12)]
       实际得到: [('name', 'tom'), ('age', 12)]
[PASS] D14 反例: items() 视图是动态的，后加的键也能看到
       示例声称: [('a', 1), ('b', 2)]
       实际得到: [('a', 1), ('b', 2)]
[PASS] D15 反例: 'a' in map 判断的是键
       示例声称: True
       实际得到: True
[PASS] D16 反例: 'tom' in map 为 False（值是成员但 in 只看键）
       示例声称: False
       实际得到: False
[PASS] D17 反例: 取不存在的键抛 KeyError
       预期异常: KeyError
       实际得到: KeyError: 'z'
[PASS] D18 反例: .get() 取不到返回 None 而不是报错
       示例声称: None
       实际得到: None
[PASS] D19 反例: .get('z', 0) 可给默认值
       示例声称: 0
       实际得到: 0

========================================================================
E. examples/comprehension/ —— 2 个文件
========================================================================
[PASS] E1 list.py: [el*2 for el in [1,2,3,4]]
       示例声称: [2, 4, 6, 8]
       实际得到: [2, 4, 6, 8]
[PASS] E2 list.py: 与 for 循环逐个 append 等价
       示例声称: [2, 4, 6, 8]
       实际得到: [2, 4, 6, 8]
[PASS] E3 list-filter.py: 筛选偶数再乘 2
       示例声称: [4, 8, 12, 16, 20, 24, 28]
       实际得到: [4, 8, 12, 16, 20, 24, 28]
[PASS] E4 list-filter.py: 注释写的 7 个结果数量正确
       示例声称: 7
       实际得到: 7
[PASS] E5 list-filter.py: range(1,15) 到 14 结束、不含 15
       示例声称: 14
       实际得到: 14
[PASS] E6 反例: 推导式支持 else（三目）
       示例声称: [0, 1, -2, 3]
       实际得到: [0, 1, -2, 3]
[PASS] E7 反例: 嵌套推导式外层先行
       示例声称: [[1, 2], [2, 4]]
       实际得到: [[1, 2], [2, 4]]
[PASS] E8 反例: 字典推导式 {k: v}
       示例声称: {0: 0, 1: 2}
       实际得到: {0: 0, 1: 2}
[PASS] E9 反例: 集合推导式自动去重
       示例声称: {0, 1}
       实际得到: {0, 1}
[PASS] E10 反例: 推导式有独立作用域，循环变量不外泄
       示例声称: 1
       实际得到: 1

========================================================================
F. examples/statement/ —— 10 个文件
========================================================================
[PASS] F1 break.py: 第一个 >2 的元素下标是 2
       示例声称: 'first element greater 2 index:  2\n'
       实际得到: 'first element greater 2 index:  2\n'
[PASS] F2 break.py: 退出码 0
       示例声称: 0
       实际得到: 0
[PASS] F3 continue.py: continue 只跳过本次迭代余下部分
       示例声称: 'odd number:  1\neven number:  2\nodd number:  3\neven number:  4\n'
       实际得到: 'odd number:  1\neven number:  2\nodd number:  3\neven number:  4\n'
[PASS] F4 continue.py: 'this code never execute' 一次都没打印
       示例声称: False
       实际得到: False
[PASS] F5 while.py: 手写下标循环
       示例声称: '1\n2\n3\n'
       实际得到: '1\n2\n3\n'
[PASS] F6 for.py: for 直接遍历列表元素
       示例声称: '1\n2\n3\n'
       实际得到: '1\n2\n3\n'
[PASS] F7 for-else.py: 完整输出（含 else 走与不走两种）
       示例声称: '除零被捕获\nfinally 总会执行\ni = 0\ni = 1\ni = 2\n循环正常结束，未被 break 打断\ni = 0\n'
       实际得到: '除零被捕获\nfinally 总会执行\ni = 0\ni = 1\ni = 2\n循环正常结束，未被 break 打断\ni = 0\n'
[PASS] F8 for-else.py: 没 break 时 else 执行
       示例声称: True
       实际得到: True
[PASS] F9 for-else.py: break 之后 else 不执行
       示例声称: False
       实际得到: False
[PASS] F10 if.py: 送 7 只打印提示、不打印奇偶结论（提示语含尾随空格）
       示例声称: 'enter a number: '
       实际得到: 'enter a number: '
[PASS] F11 else.py: 送 7 走 else 分支
       示例声称: 'enter a number: a is odd number\n'
       实际得到: 'enter a number: a is odd number\n'
[PASS] F12 elif.py: 送 7 命中 else 分支 positive
       示例声称: 'enter a number: positive\n'
       实际得到: 'enter a number: positive\n'
[PASS] F13 try.py: 送 7 不抛异常，打印的是 'x is a valid number: 7'
       示例声称: 'Please enter a number: x is a valid number: 7\n'
       实际得到: 'Please enter a number: x is a valid number: 7\n'
[PASS] F14 try.py: 送 'abc' 时被 except ValueError 抓住
       示例声称: ('Please enter a number: Oops! That was not a valid number.', 0)
       实际得到: ('Please enter a number: Oops! That was not a valid number.', 0)
[PASS] F15 finally.py: try 正常结束后 finally 仍执行
       示例声称: 'Please enter a number: x is a valid number: 7\nover\n'
       实际得到: 'Please enter a number: x is a valid number: 7\nover\n'
[PASS] F16 try/except/else/finally：有异常时顺序 = try, except, finally（不走 else）
       示例声称: "['try', 'except', 'finally']"
       实际得到: "['try', 'except', 'finally']"
[PASS] F17 无异常时才走 else
       示例声称: "['try', 'else', 'finally']"
       实际得到: "['try', 'else', 'finally']"
[PASS] F18 try.py 裸 except 连 EOFError 都吞（所以 run-all.sh 里它显示 exit 0）
       示例声称: ('caught', 0)
       实际得到: ('caught', 0)
[PASS] F19 反例: 改成 except ValueError 后 EOFError 会逃出去（exit 1）
       示例声称: 1
       实际得到: 1
[PASS] F20 反例: except ValueError 仍能抓住 'abc'
       示例声称: ('caught', 0)
       实际得到: ('caught', 0)
[PASS] F21 反例: 裸 except 会吞掉 KeyboardInterrupt（Ctrl+C 失灵）
       示例声称: ('swallowed', 0)
       实际得到: ('swallowed', 0)

========================================================================
G. examples/function/ —— 7 个文件
========================================================================
[PASS] G1 def.py: fib(10) 打印 0 1 1 2 3 5 8
       示例声称: 'enter a number:0 1 1 2 3 5 8 \n'
       实际得到: 'enter a number:0 1 1 2 3 5 8 \n'
[PASS] G2 def.py: a, b = b, a+b 同步赋值（斐波那契递推）
       示例声称: (1, 1)
       实际得到: (1, 1)
[PASS] G3 def.py: 函数没有 return 时返回 None
       示例声称: None
       实际得到: None
[PASS] G4 def_default_arg.py: hi('tom') 用默认 time
       示例声称: 'morning tom\n'
       实际得到: 'morning tom\n'
[PASS] G5 def_default_arg.py: 默认值存在 __defaults__
       示例声称: ('morning',)
       实际得到: ('morning',)
[PASS] G6 反例: 可变默认参数跨调用共享，三次是 [1]/[1,1]/[1,1,1]
       示例声称: '[1]\n[1, 1]\n[1, 1, 1]'
       实际得到: '[1]\n[1, 1]\n[1, 1, 1]'
[PASS] G7 反例: 用 None 哨兵后每次都是 [1]
       示例声称: '[1]\n[1]'
       实际得到: '[1]\n[1]'
[PASS] G8 def_key_arg.py: 关键字实参顺序无关
       示例声称: 'morning tom\nmorning tom\n'
       实际得到: 'morning tom\nmorning tom\n'
[PASS] G9 def_map.py: **info 收集多余关键字参数
       示例声称: "{'name': 'tom', 'age': 10, 'city': 'berlin', 'sex': 'man'}\n"
       实际得到: "{'name': 'tom', 'age': 10, 'city': 'berlin', 'sex': 'man'}\n"
[PASS] G10 def_map.py: **kwargs 的类型是 dict
       示例声称: 'dict'
       实际得到: 'dict'
[PASS] G11 def_return.py: 'tom lee hooker'.title()
       示例声称: 'Tom Lee Hooker\n'
       实际得到: 'Tom Lee Hooker\n'
[PASS] G12 def_return.py: title() 每个单词首字母大写
       示例声称: 'Hello World'
       实际得到: 'Hello World'
[PASS] G13 def_tuple.py: *names 收集成元组
       示例声称: 'name: tom\nname: locke\nname: jerry\n'
       实际得到: 'name: tom\nname: locke\nname: jerry\n'
[PASS] G14 def_tuple.py: *args 的类型是 tuple
       示例声称: 'tuple'
       实际得到: 'tuple'
[PASS] G15 反例: *args 与 **kwargs 可同时出现
       示例声称: (('a',), {'b': 1})
       实际得到: (('a',), {'b': 1})
[PASS] G16 反例: 位置参数不能跟在关键字参数之后
       预期异常: SyntaxError
       实际得到: SyntaxError: positional argument follows keyword argument (<s>, line 2)

========================================================================
H. examples/class/ —— 12 个文件
========================================================================
[PASS] H1 class-attr.py: C.type 取类属性
       示例声称: 'C'
       实际得到: 'C'
[PASS] H2 class-attr.py: 实例属性遮蔽同名类属性
       示例声称: 'c1'
       实际得到: 'c1'
[PASS] H3 class-attr.py: 另一个实例取自己的值
       示例声称: 'c2'
       实际得到: 'c2'
[PASS] H4 反例: 遮蔽只写进实例 __dict__，类属性不变
       示例声称: (True, 'C')
       实际得到: (True, 'C')
[PASS] H5 class-attr-over.py: 未遮蔽时实例透传到类属性
       示例声称: 'person\nperson\ntom eat\nperson\njack eat\n'
       实际得到: 'person\nperson\ntom eat\nperson\njack eat\n'
[PASS] H6 init.py: __init__ 初始化实例属性
       示例声称: 'tom, age:10\ntom eat\njack, age:3\njack eat\n'
       实际得到: 'tom, age:10\ntom eat\njack, age:3\njack eat\n'
[PASS] H7 instance.py: self 指实例，c1.hi() 输出 hi
       示例声称: 'hi\n'
       实际得到: 'hi\n'
[PASS] H8 define.py: 无 self 的方法能通过类调用
       示例声称: 'hi\n'
       实际得到: 'hi\n'
[PASS] H9 反例: 同一个无 self 方法用实例调用会 TypeError
       预期异常: TypeError
       实际得到: TypeError: _NoSelf.hi() takes 0 positional arguments but 1 was given
[PASS] H10 class_attr_class.py: C.__class__ == C 为 False、实例为 True
       示例声称: 'False\nTrue\n'
       实际得到: 'False\nTrue\n'
[PASS] H11 class_attr_class.py: 实例的 __class__ 就是 C
       示例声称: True
       实际得到: True
[PASS] H12 反例: C.__class__ is type
       示例声称: True
       实际得到: True
[PASS] H13 class_attr_doc.py: 类与实例读到的 __doc__ 是同一个对象
       示例声称: True
       实际得到: True
[PASS] H14 class_attr_doc.py: __doc__ 取到类体第一个字符串
       示例声称: 'doc of D'
       实际得到: 'doc of D'
[PASS] H15 反例: 没有 docstring 的类 __doc__ 是 None
       示例声称: None
       实际得到: None
[PASS] H16 extends.py: super().__init__(name) 先建父类属性
       示例声称: 'tom.name: tom\ntom.school: s1\nlearn\n'
       实际得到: 'tom.name: tom\ntom.school: s1\nlearn\n'
[PASS] H17 extends.py: 子类实例同时有父类与自己的属性
       示例声称: ('tom', 's1')
       实际得到: ('tom', 's1')
[PASS] H18 反例: 不调 super().__init__ 时 self.name 不存在
       预期异常: AttributeError
       实际得到: AttributeError: '_StudentNoSuper' object has no attribute 'name'
[PASS] H19 method.py: g = c1.hi 之后 g() 仍绑同一个实例
       示例声称: 'hi tom\nhi tom\n'
       实际得到: 'hi tom\nhi tom\n'
[PASS] H20 method.py: 实例方法的 __self__ 就是该实例
       示例声称: True
       实际得到: True
[PASS] H21 method.py: 类上取到的是普通函数，要自己传 self
       示例声称: 'hi tom'
       实际得到: 'hi tom'
[PASS] H22 method_assign.py: 实例调用与类调用等价
       示例声称: 'hi tom\nhi tom\n'
       实际得到: 'hi tom\nhi tom\n'
[PASS] H23 method_define_outside.py: 类体外函数赋给类属性，五种调用方式都通
       示例声称: 'hi tom\nhi tom\nhi tom\nhi tom\nhi tom\n'
       实际得到: 'hi tom\nhi tom\nhi tom\nhi tom\nhi tom\n'
[PASS] H24 method_define_outside.py: C1.hi is hi（同一个函数对象，未包装）
       示例声称: True
       实际得到: True
[PASS] H25 define-with-statement.py: 类体语句在定义时执行，不等实例化
       示例声称: 'test\n1\n2\n3\n4\n5\n6\n7\n8\n9\nmain\n'
       实际得到: 'test\n1\n2\n3\n4\n5\n6\n7\n8\n9\nmain\n'
[PASS] H26 define-with-statement.py: __module__ 在类体里可取到模块名（模块层取不到）
       示例声称: 'module in class body: __main__'
       实际得到: 'module in class body: __main__'
[PASS] H27 反例: 类体里 __name__ 与 __module__ 都能取到模块名（后者是非主流写法）
       示例声称: 'body runs\nmain\nname-main\nmodule __name__ = __main__'
       实际得到: 'body runs\nmain\nname-main\nmodule __name__ = __main__'

========================================================================
I. examples/api/ —— 3 个文件
========================================================================
[PASS] I1 list-operation.py: append(len(list)+1)
       示例声称: 'list: [1, 2, 3, 4]\nlist.append(len(list)+1): [1, 2, 3, 4, 5]\n'
       实际得到: 'list: [1, 2, 3, 4]\nlist.append(len(list)+1): [1, 2, 3, 4, 5]\n'
[PASS] I2 list-operation.py: len 在 append 之前求值
       示例声称: 5
       实际得到: 5
[PASS] I3 os.py: os.path.join 用当前平台分隔符拼接
       示例声称: '/a\\b\\c'
       实际得到: '/a\\b\\c'
[PASS] I4 os.py: 本机 os.sep 就是 join 实际使用的分隔符
       示例声称: '\\'
       实际得到: '\\'
[PASS] I5 os.py: isabs('/a/b/c') 为 True
       示例声称: 'True'
       实际得到: 'True'
[PASS] I6 os.py: isabs('./a') 为 False
       示例声称: 'False'
       实际得到: 'False'
[PASS] I7 os.py: getcwd/abspath 输出随机器变化（证据天然不可复现）
       示例声称: True
       实际得到: True
[PASS] I8 string-operation.py: 完整输出（含拼接与 rstrip 两行）
       示例声称: "str: hello world\nstr.title(): Hello World\nstr.upper(): HELLO WORLD\nstr.lower(): hello world\n'a''b': ab\n'1' + text: 1hello world\nstr.rstrip(): \thello world\n"
       实际得到: "str: hello world\nstr.title(): Hello World\nstr.upper(): HELLO WORLD\nstr.lower(): hello world\n'a''b': ab\n'1' + text: 1hello world\nstr.rstrip(): \thello world\n"
[PASS] I9 string-operation.py: 'a''b' 相邻拼接为 ab
       示例声称: 'ab'
       实际得到: 'ab'
[PASS] I10 string-operation.py: '1' + str 前缀拼接
       示例声称: '1hello world'
       实际得到: '1hello world'
[PASS] I11 string-operation.py: rstrip 只删右侧空白
       示例声称: '\thello world'
       实际得到: '\thello world'
[PASS] I12 反例: lstrip 只删左侧、strip 删两侧
       示例声称: ('hello world  ', 'hello world')
       实际得到: ('hello world  ', 'hello world')
[PASS] I13 反例: 标签写 str.rstripe() 是拼写错误，真实方法名是 rstrip
       示例声称: ('rstrip', False)
       实际得到: ('rstrip', False)

========================================================================
J. examples/_draft/ —— 10 个文件
========================================================================
[PASS] J1 11-define-variable.py 是 0 字节空文件，运行无任何输出
       示例声称: ''
       实际得到: ''
[PASS] J2 12-use-variable.py: 整数、浮点、复数三段完整输出
       示例声称: '2 + 2: 4\n2 - 2: 0\n2 * 2: 4\n17 / 3: 5.666666666666667\n17 // 3: 5\n17 % 3: 2\n2 ** 3: 8\n2.0 + 2: 4.0\n2.0 - 2: 0.0\n2 * 2.0: 4.0\n17.0 / 3: 5.666666666666667\n17.0 // 3: 5.0\n17.0 % 3: 2.0\n2 ** 3.1: 8.574187700290345\n 2+3j+4j (2+7j)\n2+3j*4j (-10+0j)\n'
       实际得到: '2 + 2: 4\n2 - 2: 0\n2 * 2: 4\n17 / 3: 5.666666666666667\n17 // 3: 5\n17 % 3: 2\n2 ** 3: 8\n2.0 + 2: 4.0\n2.0 - 2: 0.0\n2 * 2.0: 4.0\n17.0 / 3: 5.666666666666667\n17.0 // 3: 5.0\n17.0 % 3: 2.0\n2 ** 3.1: 8.574187700290345\n 2+3j+4j (2+7j)\n2+3j*4j (-10+0j)\n'
[PASS] J3 12-use-variable.py: 浮点参与后 // 仍是取整但类型变 float
       示例声称: '5.0'
       实际得到: '5.0'
[PASS] J4 12-use-variable.py: 2 ** 3.1 允许非整数指数
       示例声称: 8.574187700290345
       实际得到: 8.574187700290345
[PASS] J5 12-use-variable.py: 2+3j+4j 虚部相加
       示例声称: '(2+7j)'
       实际得到: '(2+7j)'
[PASS] J6 12-use-variable.py: 2+3j*4j —— * 优先于 +，3j*4j = -12+0j
       示例声称: '(-10+0j)'
       实际得到: '(-10+0j)'
[PASS] J7 21.types-number.py: 4/2 得 2.0 不是 2
       示例声称: '2.0'
       实际得到: '2.0'
[PASS] J8 21.types-number.py: 3/2. 得 1.5
       示例声称: '1.5'
       实际得到: '1.5'
[PASS] J9 21.types-number.py: 3//2 得 1
       示例声称: '1'
       实际得到: '1'
[PASS] J10 反例: 注释说 // 「return a integer」，但 3//2. 返回 1.0（float）
       示例声称: 'float'
       实际得到: 'float'
[PASS] J11 23.types-list.py: arr = [1,2,3,4],[5,6,7,8] 是元组套两个列表
       示例声称: '([1, 2, 3, 4], [5, 6, 7, 8])'
       实际得到: '([1, 2, 3, 4], [5, 6, 7, 8])'
[PASS] J12 23.types-list.py: 切片 [0:2] / [2:] / [:-1]
       示例声称: ('[1, 2]', '[3, 4]', '[1, 2, 3]')
       实际得到: ('[1, 2]', '[3, 4]', '[1, 2, 3]')
[PASS] J13 23.types-list.py: [1,2]+[3,4] 拼接
       示例声称: [1, 2, 3, 4]
       实际得到: [1, 2, 3, 4]
[PASS] J14 23.types-list.py: [1]*10 重复
       示例声称: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
       实际得到: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
[PASS] J15 31-if.py: 送 7 走 else
       示例声称: 'please enter a number: x is odd number\n'
       实际得到: 'please enter a number: x is odd number\n'
[PASS] J16 32-for.py: fib(10) —— 文件名写 for，内容却是函数
       示例声称: '0 1 1 2 3 5 8 \n'
       实际得到: '0 1 1 2 3 5 8 \n'
[PASS] J17 41-function.py: make_incrementor 返回闭包
       示例声称: '1\n2\n3\n'
       实际得到: '1\n2\n3\n'
[PASS] J18 41-function.py: 闭包细胞存住 n
       示例声称: 1
       实际得到: 1
[PASS] J19 41-function.py: lambda 的 __name__ 是 '<lambda>'
       示例声称: '<lambda>'
       实际得到: '<lambda>'
[PASS] J20 42-function-attributes.py: __doc__ 可写、写后立即生效
       示例声称: True
       实际得到: True
[PASS] J21 42-function-attributes.py: __defaults__ 是元组
       示例声称: "('tom',)"
       实际得到: "('tom',)"
[PASS] J22 42-function-attributes.py: __code__.co_varnames 只含局部变量
       示例声称: "('tom',)"
       实际得到: "('tom',)"
[PASS] J23 反例: __closure__ 对非闭包函数是 None
       示例声称: None
       实际得到: None
[PASS] J24 反例: 无注解时 __annotations__ 是空 dict
       示例声称: {}
       实际得到: {}
[PASS] J25 反例: 无仅关键字默认值时 __kwdefaults__ 是 None
       示例声称: None
       实际得到: None
[PASS] J26 反例: 函数可挂自定义属性进 __dict__
       示例声称: {'a': {'a': 1}}
       实际得到: {'a': {'a': 1}}
[PASS] J27 反例: 示例打印 __globals__ 会把本机绝对路径写进证据（建议删）
       示例声称: True
       实际得到: True
[PASS] J28 4x-lambda.py: for w, len(w) 同行打印
       示例声称: 'cat 3\nwindow 6\ndefenestrate 12\n'
       实际得到: 'cat 3\nwindow 6\ndefenestrate 12\n'
[PASS] J29 反例: 文件名写 lambda，内容没有任何 lambda
       示例声称: True
       实际得到: True

========================================================================
K. examples/tutorial/ + examples/mnist/ —— 2 个文件
========================================================================
[PASS] K1 tutorial/print.py: print(1+2) 先求值再传参
       示例声称: '3\nhello world!\n'
       实际得到: '3\nhello world!\n'
[PASS] K2 mnist/main.py: 必须 cd examples 后用 -m 调用（D-08）
       示例声称: 0
       实际得到: 0
[PASS] K3 mnist/main.py: 前四行输出
       示例声称: '训练集图片: [1, 2, 3]\n训练集标签: [0, 1, 2]\n测试集图片: [4, 5]\n测试集标签: [1, 0]\n'
       实际得到: '训练集图片: [1, 2, 3]\n训练集标签: [0, 1, 2]\n测试集图片: [4, 5]\n测试集标签: [1, 0]\n'
[PASS] K4 mnist/main.py: 直接按路径跑必失败
       示例声称: 'raises'
       实际得到: 'raises'
[PASS] K5 mnist/data.py: 只导出 load_data 一个公开名
       示例声称: "['load_data']"
       实际得到: "['load_data']"
[PASS] K6 mnist/data.py: 只有定义没有 print，运行无输出
       示例声称: ''
       实际得到: ''

========================================================================
L. 跨示例的反模式（走查新增，教程未声明）
========================================================================
[PASS] L1 反例: 变量名 list / map / str 会遮蔽内建，三处全部 TypeError
       示例声称: 3
       实际得到: 3
[PASS] L2 回归: 用内建名当变量名的示例文件应为 0 个（D-30 已修）
       示例声称: 0
       实际得到: 0
[PASS] L3 反例: round(2.5) 是 2 不是 3（银行家舍入）
       示例声称: 2
       实际得到: 2
[PASS] L4 反例: round(3.5) 是 4
       示例声称: 4
       实际得到: 4
[PASS] L5 反例: round(0.5) 是 0
       示例声称: 0
       实际得到: 0
[PASS] L6 反例: True + True == 2（bool 是 int 子类）
       示例声称: 2
       实际得到: 2
[PASS] L7 反例: 1 == True 但 1 is True 为 False
       示例声称: (True, False)
       实际得到: (True, False)
[PASS] L8 反例: bool('False') 为 True（非空字符串即真）
       示例声称: True
       实际得到: True
[PASS] L9 反例: nan != nan
       示例声称: False
       实际得到: False
[PASS] L10 反例: 0.0 == -0.0 为 True
       示例声称: True
       实际得到: True
[PASS] L11 反例: [] and 1 返回 [] 不是 False
       示例声称: []
       实际得到: []
[PASS] L12 反例: 1 or 2 返回 1 不是 True
       示例声称: 1
       实际得到: 1
[PASS] L13 反例: 'a' + 1 抛 TypeError，而 JS 会得到 'a1'
       预期异常: TypeError
       实际得到: TypeError: can only concatenate str (not "int") to str
[PASS] L14 反例: int('3.5') 抛 ValueError，不能直接解析小数字符串
       示例声称: 'raises'
       实际得到: 'raises'

========================================================================
总计 256 条断言: 256 PASS / 0 FAIL
全部通过。
