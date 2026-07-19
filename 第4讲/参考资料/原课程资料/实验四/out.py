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
    """从hotel.csv中读取数据，并返回DataFrame"""
    df = pd.read_csv(path)  # 读取CSV文件
    return df  # 返回DataFrame


# 2. 构建Dataset类
class CommentDataset(Dataset):
    """BERT输入数据封装"""
    def __init__(self, comments, labels, tokenizer, max_len=128):
        self.comments = comments  # 文本列表
        self.labels = labels      # 标签列表
        self.tokenizer = tokenizer  # 用于文本编码
        self.max_len = max_len    # 文本最大长度

    def __len__(self):
        return len(self.comments)

    def __getitem__(self, idx):
        text = str(self.comments[idx])
        label = int(self.labels[idx])

        # 使用tokenizer编码文本为input_ids与attention_mask
        encoding = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"  # 返回PyTorch张量
        )

        # 去除多余维度（tokenizer返回形状为[1, max_len]，需转为[max_len]）
        input_ids = encoding["input_ids"].squeeze(0)
        attention_mask = encoding["attention_mask"].squeeze(0)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": torch.tensor(label, dtype=torch.long)  # 标签转为张量
        }


# 3. 模型训练函数
def train_model(model, dataloader, optimizer, device):
    """完成模型的训练循环"""
    model.train()  # 切换到训练模式
    total_loss = 0

    for batch in tqdm(dataloader, desc="训练中"):
        # 提取input_ids, attention_mask, labels并放入device
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        # 梯度清零（避免累积上一轮的梯度）
        optimizer.zero_grad()

        # 前向传播，计算loss
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        loss = outputs.loss  # 获取损失值

        # 反向传播：计算梯度
        loss.backward()

        # 参数更新：根据梯度调整权重
        optimizer.step()

        # 累加loss
        total_loss += loss.item()

    return total_loss / len(dataloader)


# 4. 主函数
def main():
    # 加载数据
    df = load_data("hotel.csv")  # 确保hotel.csv在当前目录

    # 划分训练/测试集
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df["Comment"], df["Label"], test_size=0.2, random_state=42
    )

    # 初始化tokenizer与模型
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    model = BertForSequenceClassification.from_pretrained("bert-base-chinese", num_labels=2)

    # 构建Dataset和DataLoader
    train_dataset = CommentDataset(train_texts.tolist(), train_labels.tolist(), tokenizer)
    val_dataset = CommentDataset(val_texts.tolist(), val_labels.tolist(), tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4)

    # 优化器与设备
    optimizer = AdamW(model.parameters(), lr=2e-5)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # 训练若干轮
    for epoch in range(3):
        loss = train_model(model, train_loader, optimizer, device)
        print(f"第 {epoch+1} 轮训练 Loss = {loss:.4f}")

    # 简单测试
    model.eval()
    sample = [
        "酒店位置很好，服务态度也不错，房间干净。",
        "早餐非常难吃，服务员态度也不好。",
        "交通方便，地铁口出来就到，下次还会住。",
        "房间又小又脏，空调坏了，体验极差！",
        "价格公道，性价比高，推荐入住！",
        "前台人员不热情，等了半小时才给房卡。"
    ]
    with torch.no_grad():  # 关闭梯度计算，节省内存
        for text in sample:
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()  # 取概率最大的标签
            print(f"文本：{text}")
            print(f"预测标签：{pred}（1=正面，0=负面）")
            print("-"*50)

if __name__ == "__main__":
    main()