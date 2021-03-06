# 类型


## Numbers
### 数值运算
数值计算中，常见运算符如下:

* `+`
* `-`
* `*`
* `/`
* `//` 向下取整除法
* `**` 幂运算
* `()` 表示分组

在 [REPL](./begin.md#REPL) 模式下，执行如下语句

<<< ./examples/number/operator.py


### 数值类型
除了整数，python 还支持浮点，复数和其他进制表示法。

* 浮点用来表示包含小数的数值，采用 `.` 来分隔整数和小数部分，例如 `11.1`,`10.2`
* 可采用 `_` 来分隔数值，例如 `1_000_000` 的形式来表示大整数
* 也可采用 [科学计数法](https://baike.baidu.com/item/%E7%A7%91%E5%AD%A6%E8%AE%B0%E6%95%B0%E6%B3%95/1612882?fromtitle=%E7%A7%91%E5%AD%A6%E8%AE%A1%E6%95%B0%E6%B3%95&fromid=756685&fr=aladdin) 表示大整数，例如 `1.2e10` 表示 `12_000_000_000`
* 采用 `j,J` 来表示复数的虚部，例如 `3 + 1j`，`3` 为实部，`1j` 为虚部 **注意虚部前缀必须包含数值，直接写 `3 + j` 非法。运算符对复数计算也有效**
* 通过添加 `0<进制标识>` 的形式，来表示其他进制，例如
  * `012` 表示 10 进制，python 默认采用 10 进制，所以前导 0 可忽略
  * `0b,0B` 表示二进制，例如 `0b10` 表示 10 进制 2 
  * `0o,0O` 表示八进制，例如 `0o10` 表示 10 进制 8 
  * `0x,0x` 表示十六进制，例如 `0x10` 表示 10 进制 16

在 [REPL](./begin.md#REPL) 模式下，执行如下语句，熟悉进制表示

<<< ./examples/number/converter.py

### 浮点精度
由于计算机采用二进制表示实际数值，浮点数据的表示会存在差距，所以 `0.1 + 0.1 + 0.1 == 0.3` 会返回 false, 注意此类问题。

<<< ./examples/number/float.py
## Strings
采用单引号 `'<内容>'` 或双引号 `"<内容>"` 定义字符串。

<<< ./examples/string/quote.py

可采用 `"""<内容>"""` 的方式定义多行文本

<<< ./examples/string/string-literal.py


### 转义字符
转义字符用于表示不可直接显示的内容例如换行，缩进等。
常采用 `\转义符` 的方式表示。常见的转义符如下

符号|含义
:---|:---|
`\n`| 回车
`\t`| tab 缩进
`\\`| 表示 `\`


<<< ./examples/string/escape.py

为了避免 `\` 转义可采用 `r<字符串>` 的模式阻止转义。 

<<< ./examples/string/escape-r.py

### 字符串操作
* 可采用 `<字符串>*n` 的方式重复某个字符串内容 n 次，n 为正整数
* 可采用 `<字符串> + <字符串1> + ...` 的方式连接多个字符串
  * 也可直接使用 `<字符串> <字符串1> ...` 方式合并字符串
  
<<< ./examples/string/operator.py

### 字符串切片
可以采用 `[n]` 的方式索引单个字符 
n 也可以为负值，和字符串对应关系如下

```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
```


<<< ./examples/string/index.py

也可采用形如 `[start:end]` 的方式提取一个字符串片段。`start,end` 均为可选且支持负值，表示提取从 `start` 开始长度为 `end - start` 的字符，注意当 `end` 为负数时，可将 start 根据索引关系转换为负数处理。 

<<< ./examples/string/slice.py

可以用 len 方法获取字符串长度

<<< ./examples/string/len.py

## Lists


## 知识点
