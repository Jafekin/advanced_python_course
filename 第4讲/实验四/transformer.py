import numpy as np

def softmax(x):
    """对矩阵的最后一个维度做 softmax"""
    # TODO: 实现 softmax
    # 提示：先减去最大值保证数值稳定，再 exp / sum
    pass

def scaled_dot_product_attention(Q, K, V):
    """
    计算缩放点积注意力
    参数：
        Q: shape (seq_len, d_k) - 查询矩阵
        K: shape (seq_len, d_k) - 键矩阵
        V: shape (seq_len, d_v) - 值矩阵
    返回：
        output: shape (seq_len, d_v) - 注意力输出
        attention_weights: shape (seq_len, seq_len) - 注意力权重矩阵
    """
    d_k = K.shape[-1]
    
    # TODO Step 1: 计算 Q 和 K^T 的点积
    
    # TODO Step 2: 除以 sqrt(d_k) 进行缩放
    
    # TODO Step 3: 对缩放后的分数做 softmax，得到注意力权重
    
    # TODO Step 4: 用注意力权重对 V 加权求和
    
    # return output, attention_weights
    pass

# === 测试代码 ===
np.random.seed(42)

# 模拟 3 个词，每个词的嵌入维度为 4
seq_len, d_model = 3, 4

# 模拟输入（实际中 Q/K/V 由输入乘以权重矩阵得到，这里简化）
X = np.random.randn(seq_len, d_model)

# 简化：令 Q = K = V = X（自注意力）
Q, K, V = X, X, X

output, weights = scaled_dot_product_attention(Q, K, V)

print("输入矩阵 X:")
print(X)
print("\n注意力权重矩阵（每行和为1）:")
print(weights)
print("\n注意力输出:")
print(output)