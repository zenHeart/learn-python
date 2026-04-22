# 文件操作

## 知识点
* `open` 方法
  * 打开模式 
    * `a`
    * `w`
    * `r`
    * `r+`
* `with open(filename) as f:` 的方式处理文件会自动触发 `.close` 操作
  * 写操作若没有关闭文件，写的内容不会回调到硬盘
* 文件方法
  * `f.read()` 阅读整个文件
  * `f.readline()` 阅读当行或者采用
    * `for line in  f:` 读取文件
  * `list(f), f.readlines()` 按行返回文件内容
  * `f.write(str)` 文件写入内容，非字符串需采用 `str` 方法转换后写入
  * `f.tell` 
  * `f.seek` 
* json module
  * `load` 导入
  * `dump` 导出