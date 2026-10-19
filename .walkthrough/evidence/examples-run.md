########## RUN MANIFEST ##########
date: 2026-10-20T01:35:43+08:00
python: Python 3.11.9
cwd: /c/Users/cheng/code/github/.worktrees/learn-python-stepfun-20261020
note: stdin 来自 /dev/null，调用 input() 的示例会以 EOFError 结束

================================================================
### FILE: examples/_draft/11-define-variable.py
### CMD: python "examples/_draft/11-define-variable.py" < /dev/null
--- stdout/stderr (exit=0) ---

================================================================
### FILE: examples/_draft/12-use-variable.py
### CMD: python "examples/_draft/12-use-variable.py" < /dev/null
--- stdout/stderr (exit=0) ---
2 + 2: 4
2 - 2: 0
2 * 2: 4
17 / 3: 5.666666666666667
17 // 3: 5
17 % 3: 2
2 ** 3: 8
2.0 + 2: 4.0
2.0 - 2: 0.0
2 * 2.0: 4.0
17.0 / 3: 5.666666666666667
17.0 // 3: 5.0
17.0 % 3: 2.0
2 ** 3.1: 8.574187700290345
 2+3j+4j (2+7j)
2+3j*4j (-10+0j)
================================================================
### FILE: examples/_draft/21.types-number.py
### CMD: python "examples/_draft/21.types-number.py" < /dev/null
--- stdout/stderr (exit=0) ---
2
0
4
2.0
1.5
1
8
================================================================
### FILE: examples/_draft/23.types-list.py
### CMD: python "examples/_draft/23.types-list.py" < /dev/null
--- stdout/stderr (exit=0) ---
[1, 2, 3, 4]
([1, 2, 3, 4], [5, 6, 7, 8])
1
[1, 2]
[3, 4]
[1, 2, 3]
[1, 2, 3, 4]
[1, 2, 3, 4]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
================================================================
### FILE: examples/_draft/31-if.py
### CMD: python "examples/_draft/31-if.py" < /dev/null
--- stdout/stderr (exit=1) ---
please enter a number: Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\_draft\31-if.py", line 1, in <module>
    x=int(input('please enter a number: '))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
================================================================
### FILE: examples/_draft/32-for.py
### CMD: python "examples/_draft/32-for.py" < /dev/null
--- stdout/stderr (exit=0) ---
0 1 1 2 3 5 8 
================================================================
### FILE: examples/_draft/41-function.py
### CMD: python "examples/_draft/41-function.py" < /dev/null
--- stdout/stderr (exit=0) ---
1
2
3
================================================================
### FILE: examples/_draft/42-function-attributes.py
### CMD: python "examples/_draft/42-function-attributes.py" < /dev/null
--- stdout/stderr (exit=0) ---
 
    demo function hi
    this is a test comment
    
change comment
say
hi1 say
('tom',)
<code object say at 0x000001F2E15C0A80, file "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\_draft\42-function-attributes.py", line 16>
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x000001F2E163B010>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'C:\\Users\\cheng\\code\\github\\.worktrees\\learn-python-stepfun-20261020\\examples\\_draft\\42-function-attributes.py', '__cached__': None, 'hi': <function hi at 0x000001F2E1A5D3A0>, 'say': <function say at 0x000001F2E1A5D4E0>}
{'a': {'a': 1}}
None
{}
None
================================================================
### FILE: examples/_draft/4x-lambda.py
### CMD: python "examples/_draft/4x-lambda.py" < /dev/null
--- stdout/stderr (exit=0) ---
cat 3
window 6
defenestrate 12
================================================================
### FILE: examples/api/list-operation.py
### CMD: python "examples/api/list-operation.py" < /dev/null
--- stdout/stderr (exit=0) ---
list: [1, 2, 3, 4]
list.append(len(list)+1): [1, 2, 3, 4, 5]
================================================================
### FILE: examples/api/os.py
### CMD: python "examples/api/os.py" < /dev/null
--- stdout/stderr (exit=0) ---
/a\b\c
C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020
C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\a
True
False
================================================================
### FILE: examples/api/string-operation.py
### CMD: python "examples/api/string-operation.py" < /dev/null
--- stdout/stderr (exit=0) ---
str: hello world
str.title(): Hello World
str.upper(): HELLO WORLD
str.lower(): hello world
'a''b': ab
'1' + str: 1hello world
str.rstripe(): 	hello world
================================================================
### FILE: examples/class/class_attr_class.py
### CMD: python "examples/class/class_attr_class.py" < /dev/null
--- stdout/stderr (exit=0) ---
False
True
================================================================
### FILE: examples/class/class_attr_doc.py
### CMD: python "examples/class/class_attr_doc.py" < /dev/null
--- stdout/stderr (exit=0) ---
类注释
   示例类 C

   test
   
类注释
   示例类 C

   test
   
================================================================
### FILE: examples/class/class-attr.py
### CMD: python "examples/class/class-attr.py" < /dev/null
--- stdout/stderr (exit=0) ---
C
c1
c2
================================================================
### FILE: examples/class/class-attr-over.py
### CMD: python "examples/class/class-attr-over.py" < /dev/null
--- stdout/stderr (exit=0) ---
person
person
tom eat
person
jack eat
================================================================
### FILE: examples/class/define.py
### CMD: python "examples/class/define.py" < /dev/null
--- stdout/stderr (exit=0) ---
hi
================================================================
### FILE: examples/class/define-with-statement.py
### CMD: python "examples/class/define-with-statement.py" < /dev/null
--- stdout/stderr (exit=0) ---
test
1
2
3
4
5
6
7
8
9
main
================================================================
### FILE: examples/class/extends.py
### CMD: python "examples/class/extends.py" < /dev/null
--- stdout/stderr (exit=0) ---
tom.name: tom
tom.school: s1
learn
================================================================
### FILE: examples/class/init.py
### CMD: python "examples/class/init.py" < /dev/null
--- stdout/stderr (exit=0) ---
tom, age:10
tom eat
jack, age:3
jack eat
================================================================
### FILE: examples/class/instance.py
### CMD: python "examples/class/instance.py" < /dev/null
--- stdout/stderr (exit=0) ---
hi
================================================================
### FILE: examples/class/method.py
### CMD: python "examples/class/method.py" < /dev/null
--- stdout/stderr (exit=0) ---
hi tom
hi tom
================================================================
### FILE: examples/class/method_assign.py
### CMD: python "examples/class/method_assign.py" < /dev/null
--- stdout/stderr (exit=0) ---
hi tom
hi tom
================================================================
### FILE: examples/class/method_define_outside.py
### CMD: python "examples/class/method_define_outside.py" < /dev/null
--- stdout/stderr (exit=0) ---
hi tom
hi tom
hi tom
hi tom
hi tom
================================================================
### FILE: examples/comprehension/list.py
### CMD: python "examples/comprehension/list.py" < /dev/null
--- stdout/stderr (exit=0) ---
[2, 4, 6, 8]
================================================================
### FILE: examples/comprehension/list-filter.py
### CMD: python "examples/comprehension/list-filter.py" < /dev/null
--- stdout/stderr (exit=0) ---
[4, 8, 12, 16, 20, 24, 28]
================================================================
### FILE: examples/function/def.py
### CMD: python "examples/function/def.py" < /dev/null
--- stdout/stderr (exit=1) ---
enter a number:Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\function\def.py", line 10, in <module>
    n = int(input("enter a number:"))
            ^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
================================================================
### FILE: examples/function/def_default_arg.py
### CMD: python "examples/function/def_default_arg.py" < /dev/null
--- stdout/stderr (exit=0) ---
morning tom
================================================================
### FILE: examples/function/def_key_arg.py
### CMD: python "examples/function/def_key_arg.py" < /dev/null
--- stdout/stderr (exit=0) ---
morning tom
morning tom
================================================================
### FILE: examples/function/def_map.py
### CMD: python "examples/function/def_map.py" < /dev/null
--- stdout/stderr (exit=0) ---
{'name': 'tom', 'age': 10, 'city': 'berlin', 'sex': 'man'}
================================================================
### FILE: examples/function/def_return.py
### CMD: python "examples/function/def_return.py" < /dev/null
--- stdout/stderr (exit=0) ---
Tom Lee Hooker
================================================================
### FILE: examples/function/def_tuple.py
### CMD: python "examples/function/def_tuple.py" < /dev/null
--- stdout/stderr (exit=0) ---
name: tom
name: locke
name: jerry
================================================================
### FILE: examples/list/list_add.py
### CMD: python "examples/list/list_add.py" < /dev/null
--- stdout/stderr (exit=0) ---
origin list: [1, True, 'tom']
append list: [1, True, 'tom', 'jack']
 0 insert list: ['jack', 1, True, 'tom']
new_list: ['jack', 1, True, 'tom', 'tom']
list: ['jack', 1, True, 'tom']
[1]*5 [1, 1, 1, 1, 1]
================================================================
### FILE: examples/list/list_del.py
### CMD: python "examples/list/list_del.py" < /dev/null
--- stdout/stderr (exit=0) ---
list: [True, 'tom', 1] remove: None
list: ['tom', 1]
list: ['tom']
list: [1, True, 1] pop: tom
================================================================
### FILE: examples/list/list_init.py
### CMD: python "examples/list/list_init.py" < /dev/null
--- stdout/stderr (exit=0) ---
item: 1
item: True
item: tom
================================================================
### FILE: examples/list/list_modify.py
### CMD: python "examples/list/list_modify.py" < /dev/null
--- stdout/stderr (exit=0) ---
origin list: [1, True, 'tom']
modify list: [1, False, 'tom']
================================================================
### FILE: examples/list/list_order.py
### CMD: python "examples/list/list_order.py" < /dev/null
--- stdout/stderr (exit=0) ---
list.sort(): ['1', 'A', 'jack', 'jerry', 'tom']
sorted(list): ['1', 'A', 'jack', 'jerry', 'tom'] list: ['A', 'tom', 'jerry', 'jack', '1']
list.reverse(): ['1', 'jack', 'jerry', 'tom', 'A']
================================================================
### FILE: examples/list/list_search.py
### CMD: python "examples/list/list_search.py" < /dev/null
--- stdout/stderr (exit=0) ---
list[0]: 1
list[len(list) - 1]: tom
list[-1]: tom
list[0:2]: [1, True]
list[1:]: [True, 'tom']
list[-2:]: [True, 'tom']
================================================================
### FILE: examples/map/map_add.py
### CMD: python "examples/map/map_add.py" < /dev/null
--- stdout/stderr (exit=0) ---
map: {'name': 'tom', 'age': 12, 'birth': 2000}
================================================================
### FILE: examples/map/map_del.py
### CMD: python "examples/map/map_del.py" < /dev/null
--- stdout/stderr (exit=0) ---
map: {'age': 12}
================================================================
### FILE: examples/map/map_init.py
### CMD: python "examples/map/map_init.py" < /dev/null
--- stdout/stderr (exit=0) ---
map: {'name': 'tom', 'age': 12}
map: {'name': 'tom', 'age': 12}
================================================================
### FILE: examples/map/map_modify.py
### CMD: python "examples/map/map_modify.py" < /dev/null
--- stdout/stderr (exit=0) ---
map: {'name': 'tom', 'age': 20}
================================================================
### FILE: examples/map/map_search.py
### CMD: python "examples/map/map_search.py" < /dev/null
--- stdout/stderr (exit=0) ---
map["name"]: tom
map.items(): dict_items([('name', 'tom'), ('age', 12)])
key: name value: tom
key: age value: 12
map.keys(): dict_keys(['name', 'age'])
key: name
key: age
map.values(): dict_values(['tom', 12])
value: tom
value: 12
================================================================
### FILE: examples/mnist/data.py
### CMD: python "examples/mnist/data.py" < /dev/null
--- stdout/stderr (exit=0) ---

================================================================
### FILE: examples/mnist/main.py
### CMD: python "examples/mnist/main.py" < /dev/null
--- stdout/stderr (exit=1) ---
Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\mnist\main.py", line 5, in <module>
    from mnist.data import load_data
ModuleNotFoundError: No module named 'mnist'
================================================================
### FILE: examples/number/converter.py
### CMD: python "examples/number/converter.py" < /dev/null
--- stdout/stderr (exit=0) ---
2.3
-0.23
100000.0
0.011
1220.0
2j
0j
(-1+0j)
(1+0j)
2 11
1 1
1 1
1000000
8
64
255
================================================================
### FILE: examples/number/float.py
### CMD: python "examples/number/float.py" < /dev/null
--- stdout/stderr (exit=0) ---
False
================================================================
### FILE: examples/number/operator.py
### CMD: python "examples/number/operator.py" < /dev/null
--- stdout/stderr (exit=0) ---
4
0
6
0.6666666666666666
0
8
1
16
================================================================
### FILE: examples/statement/break.py
### CMD: python "examples/statement/break.py" < /dev/null
--- stdout/stderr (exit=0) ---
first element greater 2 index:  2
================================================================
### FILE: examples/statement/continue.py
### CMD: python "examples/statement/continue.py" < /dev/null
--- stdout/stderr (exit=0) ---
odd number:  1
even number:  2
odd number:  3
even number:  4
================================================================
### FILE: examples/statement/elif.py
### CMD: python "examples/statement/elif.py" < /dev/null
--- stdout/stderr (exit=1) ---
enter a number: Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\statement\elif.py", line 1, in <module>
    a = int(input("enter a number: "))
            ^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
================================================================
### FILE: examples/statement/else.py
### CMD: python "examples/statement/else.py" < /dev/null
--- stdout/stderr (exit=1) ---
enter a number: Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\statement\else.py", line 1, in <module>
    a = int(input('enter a number: '))
            ^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
================================================================
### FILE: examples/statement/finally.py
### CMD: python "examples/statement/finally.py" < /dev/null
--- stdout/stderr (exit=0) ---
Please enter a number: Oops!  That was no valid number.
over
================================================================
### FILE: examples/statement/for.py
### CMD: python "examples/statement/for.py" < /dev/null
--- stdout/stderr (exit=0) ---
1
2
3
================================================================
### FILE: examples/statement/for-else.py
### CMD: python "examples/statement/for-else.py" < /dev/null
--- stdout/stderr (exit=0) ---
除零被捕获
finally 总会执行
i = 0
i = 1
i = 2
循环正常结束，未被 break 打断
i = 0
================================================================
### FILE: examples/statement/if.py
### CMD: python "examples/statement/if.py" < /dev/null
--- stdout/stderr (exit=1) ---
enter a number: Traceback (most recent call last):
  File "C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\statement\if.py", line 1, in <module>
    a = int(input('enter a number: '))
            ^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
================================================================
### FILE: examples/statement/try.py
### CMD: python "examples/statement/try.py" < /dev/null
--- stdout/stderr (exit=0) ---
Please enter a number: Oops!  That was no valid number.
================================================================
### FILE: examples/statement/while.py
### CMD: python "examples/statement/while.py" < /dev/null
--- stdout/stderr (exit=0) ---
1
2
3
================================================================
### FILE: examples/string/escape.py
### CMD: python "examples/string/escape.py" < /dev/null
--- stdout/stderr (exit=0) ---
test
break line
hello	world!
\
================================================================
### FILE: examples/string/escape-r.py
### CMD: python "examples/string/escape-r.py" < /dev/null
--- stdout/stderr (exit=0) ---
test\nbreak line
hello\tworld!
\\
================================================================
### FILE: examples/string/index.py
### CMD: python "examples/string/index.py" < /dev/null
--- stdout/stderr (exit=0) ---
p
p
n
================================================================
### FILE: examples/string/len.py
### CMD: python "examples/string/len.py" < /dev/null
--- stdout/stderr (exit=0) ---
6
================================================================
### FILE: examples/string/operator.py
### CMD: python "examples/string/operator.py" < /dev/null
--- stdout/stderr (exit=0) ---
banana
banana
banana
================================================================
### FILE: examples/string/quote.py
### CMD: python "examples/string/quote.py" < /dev/null
--- stdout/stderr (exit=0) ---
hello world!
hello world!
"Isn't," they said.
================================================================
### FILE: examples/string/slice.py
### CMD: python "examples/string/slice.py" < /dev/null
--- stdout/stderr (exit=0) ---
py
o
python
pytho

python
================================================================
### FILE: examples/string/string-literal.py
### CMD: python "examples/string/string-literal.py" < /dev/null
--- stdout/stderr (exit=0) ---
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
================================================================
### FILE: examples/tutorial/print.py
### CMD: python "examples/tutorial/print.py" < /dev/null
--- stdout/stderr (exit=0) ---
3
hello world!
