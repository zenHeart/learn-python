# 函数

通过定义函数我们可以实现代码块的复用。本节详细讲解函数的使用。
## def
采用 `def` 定义函数

```
def <函数名>(参数[=默认值1],...):
    函数体
```

例如:

```python
def hi(name,time='morning'):
    print(time+" " + name + "!")
```
## 函数调用
定义的函数可以采用如下三种方式调用
1. 直接调用 `hi('tom','morning')`
2. 关键字调用 `hi(time='morning'，name='tom',)`
    > 注意关键字调用可以不按照参数顺序赋值参数

## 返回值
默认函数返回 `None` 可以利用 `return` 语句返回参数,参见示例

<<< ./examples/function/def_return.py

## 任意个数参数
采用 `*形参名` 可以支持传入变参,传入的参数以元组方式存储

<<< ./examples/function/def_tuple.py

## 任意各数字典参数
采用 `**形参名` 可以支持关键字参数传入

<<< ./examples/function/def_map.py


## 知识点
* 函数属性，详见 [函数属性](https://docs.python.org/3/reference/datamodel.html)
* [ ] 函数格式
   ```python
   def <函数名>(参数1，参数2，...):
      # 可选内容
      """
      函数文档
      """
      函数体
   ```
* [ ] 作用域搜索顺序
  * [ ] 函数内变量
  * [ ] 全局变量
  * [ ] 内建变量
  * [ ] 采用 global 定义全局变量
  * [ ] 采用 nonlocal 表示引用全局变量，而非局部变量
* [ ] return 
  * [ ] 函数默认返回 `None`
  * [ ] return 返回斐波那契数组
* [ ] 参数定义
  * [ ] 定位参数 `arg1 = default1, arg2 = default2, ...`
    * [ ] 调用的参数可以只传入部分
    * [ ] 参数只在初次初始化有效
    * [ ] 参数为对象时，会导致值的累加，可采用 None 清空数据
  * [ ] keyword arguments, 利用参数名指定参数
    * [ ] 关键字参数必须在定位参数之后
    * [ ] 定义 `*arg` 提取所有剩余的定位参数
    * [ ] 定义 `**arg` 提取所有剩余的关键字参数
    * [ ] `**arg` 必须在 `*arg` 之后
  * [ ] 显示申明定位参数和关键字参数的传入, `/,*` 用于限制函数的调用方式
    * [ ] 默认先定位参数，后接关键字参数
    * [ ] `/` 可选后接定位参数，
      * [ ] 若出现在定位参数之后会限制函数只接收定位参数
      * [ ] 利用 `/` 解决 `**` 字典参数导致的传值冲突
    * [ ] `*` 可选后接关键字参数
      * [ ] 若出现在开头则限制函数只接受关键字参数
      * [ ] 收拢参数列表 `Arbitrary Argument Lists` 后续只能接关键字参数
      ```
      def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        Positional or keyword   |
        |                                - Keyword only
         -- Positional only
      ```
  * 参数传入
    * `*tuple` 实现元组的分别传入
    * `*map` 实现字典拆解为关键字参数逐一传入
* [ ] `lambda arg1,arg2...: expression` 定义 lambda 表达式
* [ ] 函数属性
  * [ ] `__doc__` 约定
    * [ ] 首行为概述
    * [ ] 空行后描述功能
  * [ ] `函数注解`
    * [ ] `arg: literal` 注解参数
    * [ ] ` -> literal` 注解返回值
    * [ ] `.__anotations__` 返回注解
* [ ] 编码风格
  * [ ] pep8
  * [ ] 4 空格缩进
  * [ ] 