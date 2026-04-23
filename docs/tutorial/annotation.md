# 学习标注规范

> 用统一符号标注代码中不理解的部分，便于后续定向查阅和提问。

---

## 标注符号

| 符号 | 含义 | 示例 |
|------|------|------|
| `❓` | 不懂这个语法 | `❓(a, b) = func()` 元组拆包 |
| `⚠️` | 知道是什么，但不确定用法 | `⚠️ f-string` 用法细节 |
| `🔗` | 和某处知识有关联 | `🔗 见 L1 元组拆包` |
| `✅` | 已理解 | `✅ 已掌握 print 用法` |

---

## 使用方法

### 1. 代码中标注

```python
# 标注不懂的语法
❓ from tensorflow.keras.datasets import mnist
❓ (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

### 2. 对照笔记

```markdown
## ❓ 元组拆包（Touple Unpacking）

**来源：** TensorFlow MNIST 数据加载
**疑问：** 为什么要用嵌套拆包？普通拆包不行吗？
**解答：** （学完后填写）
```

### 3. 定期归拢

把同一类的 ❓ 集中整理，形成「知识盲点清单」，逐个击破。

---

## 示例：L1 标注记录

```python
# L1 代码示例

print("hello")  # ✅ 理解

❓ name = input("请输入名字：")  # input 返回什么类型？
```

```markdown
## ❓ 待解答

| 标记 | 语法 | 来源 | 状态 |
|------|------|------|------|
| ❓ | 嵌套元组拆包 | L1 MNIST | ✅ 已解答 |
| ❓ | f-string 格式化 | L1 | 🔄 待查 |
| ❓ | `from x import y` 语法 | L1 | 🔄 待查 |

```
