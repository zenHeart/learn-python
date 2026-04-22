# tuple

## 知识点
* tuple
  * `ele,ele1,...` 定义元组 
  * 元组不可修改
  * 元组支持 `x, y, z = tuple` 分散解构
* sets
  * `{}，set()` 定义集合
  * 集合支持去重
  * 集合支持运算
    * `a - b` a 和 b 差集
    * `a | b` 并集 
    * `a & b` 交集 
    * `a ^ b` a 和 b 的交集的补集
  * `{ expression for clause } ` 操作
* dictionaries 字典，key value 的键值对
  * `{'key':value,...}` 定义字典
  * 采用 `dict([(key,value),...])` 定义字典
    * `dict(kw=val,kw1=val2,...)` 关键字模式定义字典
  * 采用 `dict comprehesions` 定义字典 `{ key: expression for claues }`
  * key 由于不可修改，可以为如下值
    * 数值
    * 字符串
    * tuple
  * 操作
    * del 删除 key value
    * val[key] 索引 字典
    * list(map) 返回 key 的 list
    * `key in map` 判断键是否存在
    * `key not in map` 判断键是否不存在
  * `k,v in maps` 提取键和值
 