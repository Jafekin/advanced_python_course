"""
BERT文本分类教学练习
目标：理解数据预处理、模型输入与训练流程。
任务：补全以下函数。
"""

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from tqdm import tqdm
"""
需要安装的包：
pip install pandas torch transformers scikit-learn tqdm
"""

# 1. 加载与划分数据
def load_data(path: str):
    """TODO: 从hotel.csv中读取数据，并返回DataFrame"""
    # df = pd.read_csv(path)
    # return df
    pass

# 2. 构建Dataset类（观察main函数的参数）
class CommentDataset(Dataset):
    """BERT输入数据封装"""
    def __init__(self, comments, labels, tokenizer, max_len=128):
        self.comments = comments  # 文本列表(从DataFrame中得到的)
        self.labels = labels      # 标签列表(从DataFrame中得到的)
        self.tokenizer = tokenizer  # 用于文本编码
        self.max_len = max_len    # 文本最大长度

    def __len__(self):
        return len(self.comments)

    def __getitem__(self, idx):
        text = str(self.comments[idx])
        label = int(self.labels[idx])

        # TODO: 用tokenizer编码文本为input_ids与attention_mask
        # 提示：tokenizer(text, padding="max_length", truncation=True, max_length=self.max_len, return_tensors="pt")
        
        # TODO: 将input_ids, attention_mask, label放入字典并返回

# 3. 模型训练函数（观察main函数的参数）
def train_model(model, dataloader, optimizer):  # 删除device参数
    """TODO: 完成模型的训练循环"""
    model.train()
    total_loss = 0
    for batch in tqdm(dataloader, desc="训练中"):
        # 提取input_ids, attention_mask, labels（无需移动到device，默认在CPU）

        # 前向传播，计算loss

        # 梯度清零
 
        # 反向传播

        # 参数更新

        # 累加loss

    return total_loss / len(dataloader)

# 4. 主函数
def main():
    # 加载数据
    df = load_data("hotel.csv")

    # 划分训练/测试集
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df["Comment"], df["Label"], test_size=0.2, random_state=42
    )

    # 初始化tokenizer与模型
    # TODO: 初始化tokenizer
    # 提示：BertTokenizer.from_pretrained("bert-base-chinese")


    # 构建Dataset和DataLoader
    train_dataset = CommentDataset(train_texts.tolist(), train_labels.tolist(), tokenizer)
    val_dataset = CommentDataset(val_texts.tolist(), val_labels.tolist(), tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4)

    # 初始化优化器
    optimizer = AdamW(model.parameters(), lr=2e-5)

    # 训练若干轮
    for epoch in range(3):
        loss = train_model(model, train_loader, optimizer)
        print(f"第 {epoch+1} 轮训练 Loss = {loss:.4f}")

    # 测试
    model.eval()
    sample = [
        "酒店位置很好，服务态度也不错，房间干净。",
        "早餐非常难吃，服务员态度也不好。",
        "交通方便，地铁口出来就到，下次还会住。",
        "房间又小又脏，空调坏了，体验极差！",
        "价格公道，性价比高，推荐入住！",
        "前台人员不热情，等了半小时才给房卡。"
    ]
    with torch.no_grad():
        for text in sample:
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            outputs = model(** inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            print(f"文本：{text}")
            print(f"预测标签：{pred}")
            print("-"*20)

if __name__ == "__main__":
    main()