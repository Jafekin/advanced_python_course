import numpy as np
import jieba
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

texts = [
    "鸡肉非常常见。",
    "牛肉富含蛋白质。",
    "猪肉通常用来制作香肠。",
    "羊肉很受欢迎。",
    "苹果是一种常见的水果。",
    "橙子是富含维生素C的水果。",
    "香蕉是好吃的的水果。",
    "草莓是用来制作甜点的水果。",
    "牛肉属于红肉类。",
    "鸡肉属于白肉类",
    "羊肉非常滋补",
    "香蕉的含糖量很高",
    "苹果的饱腹感很强",
    "草莓营养价值丰富，被誉为是水果皇后",
    "肥牛的脂肪含量很高"
]
# 标签，0代表肉类，1代表水果
labels = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]

# 分词
segmented_texts = [list(jieba.cut(text)) for text in texts]

# 构建词汇表
vocab = set(word for text in segmented_texts for word in text)
word_to_index = {word: index for index, word in enumerate(vocab)}

# 将文本转换为向量序列
text_sequences = [[word_to_index[word] for word in text if word in word_to_index] for text in segmented_texts]
# 序列填充
max_sequence_length = max(len(seq) for seq in text_sequences)
padded_sequences = pad_sequences(text_sequences, maxlen=max_sequence_length, padding='post')

# 标签独热编码
categorical_labels = to_categorical(labels)

# 划分训练集和测试集
train_x, test_x, train_y, test_y = train_test_split(padded_sequences, categorical_labels, test_size=0.30, random_state=7)

# 定义模型

model = Sequential() # 初始化Sequential模型
# 向模型中添加Embedding层
# input_dim参数设置为词汇表的大小，即不同单词的数目
# output_dim参数设置为嵌入向量的维度，这里设置为50
# input_length参数设置为输入序列的最大长度，即待分类文本的单词数
model.add(Embedding(input_dim=len(vocab), output_dim=50, input_length=max_sequence_length))
# 向模型中添加LSTM层
# 100表示LSTM层中隐藏单元的数目
model.add(LSTM(100))
# 向模型中添加Dense层
# 2表示输出层的神经元数目，因为这是一个二分类问题
# activation='softmax'表示使用softmax激活函数，它会输出0到1之间的概率分布
model.add(Dense(2, activation='softmax'))

# 编译模型，准备训练
# loss='categorical_crossentropy'表示使用分类交叉熵作为损失函数，适用于多分类问题
# optimizer='adam'表示使用Adam优化器，它是一种基于梯度下降的算法
# metrics=['accuracy']表示在训练过程中同时追踪准确率这一指标

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 训练模型
model.fit(train_x, train_y, epochs=10, batch_size=5)

# 测试集预测结果
y_pred = model.predict(test_x)
y_pred_classes = np.argmax(y_pred, axis=1)
test_y_classes = np.argmax(test_y, axis=1)

# 输出预测结果和真实结果的对比
print("Predicted values:", y_pred_classes)
print("True values     :", test_y_classes)
print("F-score: {0:.2f}".format(f1_score(test_y_classes, y_pred_classes, average='micro')))