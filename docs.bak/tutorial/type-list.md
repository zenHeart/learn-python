# list

## 知识点
* list
  * list 切片
  * list 操作
    * append 添加元素
    * 修改元素
    * 切片替换元素
    * 运算符控制元素
   * 方法
     * `list.append(x)` 尾部插入元素
       * 类似 `a[len(a):] = [x]`
       * 类似 `a =  a  +  [x]`
     * `list.extend(iterable)` 
       * 类似 `a[len(a):] = iterable`
     * `list.insert(i, x)` 
     * `list.remove(x)` 
     * `list.pop([i])`
       * `list.pop()` remove last
     * `list.clear()`
     * `list.index(x[,start,[end]])`
     * `list.count(x)` 
     * `list.sort(*,key = None, revers= False)` 
     * `list.reverse()` 
     * `list.copy()` 
 * 创建复杂列表
   * **List Comprehensions**  `[ expression for caluse ]` 
   * 支持嵌套创建多维数组
 * del 删除部分元素和变量
 * 循环技巧
  * `k,v in enumerate(list)` 提取 list 的索引和值
  * `for a,b,... in zip(list,list1,...)` 循环多个值
  * `reversed` 反向循环值
  * `sorted` 循环排序后的 list
  * 避免直接修改原始 list，利用新的 list 避免错误修改