# 输入输出

## 知识点
* `f'{var}'` 替换变量，详见 [Format Specification Mini-Language.](https://docs.python.org/3/library/string.html#formatspec)
  * `{expression}` 支持表达式
  * `{expression: n}` 设定宽度
* `format` 格式化数据
  * 支持 `{0} {kw1}.format(p1, kw1)`的方式引用定位参数和关键字参数
  * 支持 `0[key]` 方式引用字典的某项
* `str` 转换内容为字符串
* `repr` 转换内容为字符串
* string 方法
  * `rjust` 右对齐
  * `ljust` 右对齐
  * `center` 居中对齐
  * `zfill` 补 0 操作
  * 字符串插入操作，详见 [print style](https://docs.python.org/3/library/stdtypes.html#old-string-formatting)