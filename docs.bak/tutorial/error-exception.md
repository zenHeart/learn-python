# 错误和异常

## 知识点
* `Syntax error` 是解释器解析源码时的报错
* `Exceptions` 异常是程序在运行时产生的错误
  * 异常有不同的类型, 详细的内建异常参考 [built in exception](https://docs.python.org/3/library/exceptions.html#bltin-exceptions)
    * `NameError`
  * `except (Err1,Err2) :` 支持元组捕获错误
  * `except <Exception> as instance:` 提取异常实例
  * `except class:` 若子类继承父类则也会匹配父类判断
  * `except :` 表示通配
  * `Exception()` 创建一个异常类
    * args 包含传入的异常参数
    * exception 可以捕获嵌套内容抛出的异常
  * 内建异常的处理 [bltin exception](https://docs.python.org/3/library/exceptions.html#bltin-exceptions)
  * 自定义异常对象，详见 [user define exception](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)
* `else:` 子句用于无错误是的处理，例如读取文件
* `raise` 抛出一个异常
  * `raise ValueError` 等效于 `raise ValueError()`
  * `raise NameError`
  * `rais <异常> from <exceptions>` 将内部异常转换为其他异常对象
* `finally:` 子句
  * 异常捕获后触发 finally, 未捕获则执行完 finally 后继续抛出
  * 若 `exception:` 或 `else:` 字句执行抛出错误，则执行完 `finally` 后错误继续抛出
  * `finally:` 包含 `break,continue,return` 语句，异常会被忽略
  *  `try` 语句中包含 `break,continue,return` `finally` 会在推出之前执行
  *  `finally` 语句中的 return 值会覆盖`try` 语句的 return 值 
  *  `finally` 在实际编程中常用来处理 `文件或网络` 资源的释放