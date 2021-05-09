# 模块
## import

## 知识点
* 模块用于更大层级的复用
  * 主执行文件为 `main` 模块
  * `模块名` 就是文件名去除 `.py` 后缀，可以利用 `__name__` 打印模块名
* import
  * `import <module>` 打入模块 
  * `import <module> as <name>` 导入重命名 
  * `from <module> import <function_name>,...` 导入部分内容
  * `from <module> import <function_name> as <name1>` 部分内容重命名
  * `from module import *` 导入所有内容
* 模块核心
  * 采用 `__name__ == '__main__'` 判断模块为执行模式
  * 模块搜索方式
    * 先查找内建模块
    * 在 `sys.path` 查找模块
      * 脚本所在目录
      * PYTHONPATH 变量所在目录
      * 依赖默认目录
      * 可以修改 `sys.path` 来增加搜索目录
  * [`__pycache` 文件](https://docs.python.org/3/tutorial/modules.html#compiled-python-files)
  * 常用函数
    * `sys.path.append` 添加搜索路径
    * `dir` 
      * `dir()` 打印当前环境绑定的变量名
      * `dir(modulename)` 打印模块绑定的变量名
      * `import builtins;dir(builtins)` 打印内建的变量名
* packages 包，聚合多个模块
  * `__init__.py` 文件识别该目录为包
    * `__all__` 定义 `from <package> import *` 时的导入内容，没有则为全部内容
  * `import <package>.<sub_modules>...` 导入包中的子模块
  * `from <package>.<sub_modules> import <module>` 导入包中的子模块
  * `from <package>.<sub_modules> import method` 导入子模块中方法
  * 相邻导入，方便子包之间相互调用,**注意调用取决于当前包的位置**
    * `from . import <package>` 导入邻近包
    * `from .. import <package>` 上级目录的邻近包
    * `from ..<package> import <module>` 上级目录的邻近包中某模块
  * `__path__` 动态修改报包的搜索方式