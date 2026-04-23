# 模拟 mnist.load_data() 返回嵌套元组
# 真实 TensorFlow 返回的是 numpy 数组，这里用纯 Python 模拟结构

def load_data():
    """
    返回格式：(训练集, 测试集)
    训练集 = (训练图片, 训练标签)
    测试集 = (测试图片, 测试标签)
    """
    # 用简单的嵌套元组模拟数据结构
    train_images = [1, 2, 3]      # 模拟 3 张图片
    train_labels = [0, 1, 2]       # 模拟标签
    test_images = [4, 5]          # 模拟 2 张测试图片
    test_labels = [1, 0]          # 模拟测试标签

    return (train_images, train_labels), (test_images, test_labels)
