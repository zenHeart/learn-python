# 类

## 面向对象编程基础

## 类的定义
采用如下语法定义类

```
class ClassName:
   <statement-1>
   ...
   <statement-n>
```

参看示例

<<< ./examples/class/define.py



### 实例化
采用 `ClassName()` 方式实例化类

<<< ./examples/class/instance.py

:::tip
采用 c1.hi() 的方式调用类方法，解释器会按照C1.hi(c1) 的方式处理，所以一般在定义类的方法时，首个参数限定为实例自身，通常采用`self` 表示。
:::

### __init__
通常会采用 `__init__` 方法，在实例化类时，
初始化类的相关参数。

<<< ./examples/class/init.py



## 知识点
* 基础概念
  * `namespace` 
    * ptyhon 解释器启动时会创建内部命名空间，无法删除
    * 全局命名空间在模块导入时创建
    * 本地命名空间在函数申明时创建
  * `scope` 作用域是指可以直接访问的命名空间范围，为静态作用域
    * 现在本地命名空间查找
    * 全局命名空间查找
    * 内建命名空间查找
    * `nonlocal` 查找非本地空间变量
    * class 定义有独立的命名空间
    * 无 `global, nonlocal` 时，赋值语句永远在 `最内层的命名空间`，赋值语句只用于绑定名称到命名空间。
    * `import，函数定义` 绑定命名空间在内层
    * 示例说明 `nonlocal, global` 对作用域的影响
    * 
  * `.` 引用的内容都成称为属性
    * 可写的属性可以采用 `del` 删除
* 类语法
  * 申明类, 会创建一个新的本地命名空间
   ```
   class ClassName:
      <statement-1>
      ...
      <statement-N>
   ``` 
   *  可以在类中使用 `if, for` 等语法
   *  可以在类外定义成员函数  
    *  self 不是必须的只是一个惯常的约定 
  * 类对象
    * 类属性
    * 类方法
    * `__init__(self)` 定义类初始化方法
      * `__init__(self, arg1,...)` 定义类初始化传入参数
      * `self.xx` 定义类实例属性
   * 实例对象
    * 采用 `类名()` 方式，实例化
    * 实例属性可动态修改和删除
    * 区分对象方法和类方法的区别
      * 调用 `x.f` 等效于 `X.f(x)` 解释器处理了对象方调用和普通成员函数调用
    * 实例属性回覆盖类属性，若未定义实例属性会直接访问类属性
  * 继承
    ```
    class DerivedClassName(BaseClassName):
      <statement-1>
      ...
      <statement-n>
    ```
    也可使用 `class DerivedClassName(modname.BaseClass)` 从其他模块引入基类
      * 属性查找会从子类到基类
    * 多态继承
  * 类的判断
    * `isinstance`
    * `issubclass`
* 约定采用 `_xx` 定义私有属性
* `Name mangling` 采用 `__方法名` 调用基类方法可以避免子类的覆盖导致的错误。
* 采用空类创建对象结构，相比字典更方便
* 使类变为可迭代对象
  * `__iter__`
  * `__next__`