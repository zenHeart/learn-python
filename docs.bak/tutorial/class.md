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

可以直接在 class 中使用 `if, for` 等语句。

<<< ./examples/class/define-with-statement.py

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

### 实例属性和类属性
`self.name,self.age` 属于实例属性。
可以直接在类上定义共有的属性。该属性所有实例共享。

<<< ./examples/class/class-attr.py

当在类的实例上定义了和类属性同名的变量时，解释器会优先返回实例上定义的变量。

<<< ./examples/class/class-attr-over.py

### 方法
类中定义的函数可以通过类或者实例采用 `.` 号进行调用。

<<< ./examples/class/method.py

即使把方法赋值给其他变量，解释器任会根据赋值情况正常执行。

<<< ./examples/class/method_assign.py

甚至可以将方法定义在函数外。

<<< ./examples/class/method_define_outside.py

:::tip
注意上述调用方式的区别，当采用实例方式调用，或者变量赋值为实例方法进行调用时，
解释器会自动注入实例，而采用类方式或者直接使用函数方式调用时则需手动传入实例变量。
:::

### 其他属性
#### __doc__
类同样支持注释，可通过 `__doc__` 查看注释

<<< ./examples/class/class_attr_doc.py

#### __class__
`__class__` 指向实例化对象的类。

<<< ./examples/class/class_attr_class.py

::: tip
注意类对象的 `__class__` 指向内部的对象，所以 `C.__class__ == C` 返回 false, 而 `c1` 由 `C` 实例化创建，所以 `c1.__class__ == C` 返回 True 
:::

### 可迭代实例
为了使类变为可循环对象可以在内部定义 `__inter__` 方法，当使用 `for` 语句时，可使用



## 知识点
* [X] 类的语法
  
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