# 语句

## 条件判断
### if
利用形如

```
if 表达式:
  语句块
```


申明 if 语句示例判断输入是否为偶数

<<< ./examples/statement/if.py

### else
采用 else 表示额外的分支逻辑

<<< ./examples/statement/else.py

### elif
采用 elif 实现多分支判断

<<<./examples/statement/elif.py

## 循环
### for 
利用 for 循环 list 结构

<<<./examples/statement/for.py

### while
可以采用 while 实现逻辑判断循环。
采用 while 循环 list

<<<./examples/statement/while.py

### break
可以利用 break 实现跳出循环

<<<./examples/statement/break.py

### continue
break 会跳出整个 `for 或 while` 语句，若只期望
某次循环的后续执行内容，可使用 continue。

<<<./examples/statement/continue.py

## 错误捕获
### try
利用 try 捕获错误，except 中处理错误逻辑

<<< ./examples/statement/try.py

### exception

### finally
<<< ./examples/statement/finally.py



## 存疑
* [ ] for 语句中 else 语句的作用？？？
* [ ] exception 的细分处理和示例
* [ ] finally 的作用

## 知识点

* if 语句结构

  ```
  if_stmt ::=  "if" assignment_expression ":" suite
             ("elif" assignment_expression ":" suite)*
             ["else" ":" suite]
  ```
* for 语句
  
  ```
  for_stmt ::=  "for" target_list "in" expression_list ":" suite
                ["else" ":" suite]
  ```

* try 语句

  ```
  try_stmt  ::=  try1_stmt | try2_stmt
  try1_stmt ::=  "try" ":" suite
                ("except" [expression ["as" identifier]] ":" suite)+
                ["else" ":" suite]
                ["finally" ":" suite]
  try2_stmt ::=  "try" ":" suite
                "finally" ":" suite
  ```
* range(n) 定义一个循环迭代
  * range(x, y) 定义一个范围的迭代
  * range(start,end,step) 定义步长迭代
* else 只在 for 循环耗尽或 while 判断为空时执行，而非 break 状态。素数判断逻辑
* pass 表示空语句
  * 完成一个语句的正常结构
  * 空类
  * 函数占位，表示代办