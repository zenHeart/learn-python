# 从 mnist 包导入 load_data
# 这里的 mnist 是 examples/mnist/data.py 模拟的模块

# Step 1: 导入 load_data 函数
from mnist.data import load_data

# Step 2: 用嵌套拆包接收返回值
(train_images, train_labels), (test_images, test_labels) = load_data()

# Step 3: 查看结果
print("训练集图片:", train_images)
print("训练集标签:", train_labels)
print("测试集图片:", test_images)
print("测试集标签:", test_labels)

# Step 4: 验证结构
print("\n--- 结构验证 ---")
print("train_images 类型:", type(train_images).__name__)
print("train_labels 类型:", type(train_labels).__name__)
print("训练集数量:", len(train_images))
print("测试集数量:", len(test_images))
