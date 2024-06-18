import torch
from transformers import BertTokenizer

# 初始化BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

def tokenize_and_preserve_labels(sentence, text_labels):
    tokenized_sentence = []
    labels = []

    for word, label in zip(sentence, text_labels):
        # 使用BERT tokenizer对每个词进行分词
        tokenized_word = tokenizer.tokenize(word)
        n_subwords = len(tokenized_word)
        
        # 将分词后的子词添加到结果中，并保留第一个子词的标签
        tokenized_sentence.extend(tokenized_word)
        labels.extend([label] + ['O'] * (n_subwords - 1))
    
    return tokenized_sentence, labels

# 假设我们已经有了句子和标签列表
sentences = [["我", "喜欢", "北京", "的", "烤鸭", "。"], ["她", "来自", "上海", "，", "在", "华为", "工作", "。"]]
labels = [["O", "O", "B-LOC", "O", "O", "O"], ["O", "O", "B-LOC", "O", "O", "B-ORG", "O", "O"]]

tokenized_texts_and_labels = [tokenize_and_preserve_labels(sent, labs) for sent, labs in zip(sentences, labels)]

input_ids = []
attention_masks = []
label_ids = []

max_len = 128  # 假设最大序列长度为128
tag2idx = {"O": 0, "B-LOC": 1, "I-LOC": 2, "B-ORG": 3, "I-ORG": 4}  # 标签到索引的映射

for tok_sent, labs in tokenized_texts_and_labels:
    print(tok_sent,labs)
    encoding = tokenizer.encode_plus(
        tok_sent,
        is_pretokenized=True,
        max_length=max_len,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids.append(encoding['input_ids'])
    attention_masks.append(encoding['attention_mask'])
    label_ids.append([tag2idx.get(label, tag2idx["O"]) for label in labs] + [tag2idx["O"]] * (max_len - len(labs)))

# 转换为 tensor
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
label_ids = torch.tensor(label_ids)

