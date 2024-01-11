# Learning to Rank in Generative Retrieval

论文链接 [Learning to Rank in Generative Retrieval](https://arxiv.org/pdf/2306.15222.pdf)

代码地址 https://github.com/liyongqi67/LTRGR

![Alt text](image.png)

## 动机
- 如果docid是doc中的文本片段，那么同一个docid可能对应很多doc。生成式检索依靠启发式函数将预测的docid转换为doc排名列表，需要敏感的超参，且在学习框架之外。而且，生成式检索生成docid作为中间目标，而不是直接对doc进行排名。生成doc的学习目标 & doc排序目标 存在gap。因此，即便自回归模型能生成准确的docid，也未必确保最佳的doc排名。

本文提出一种用于生成式检索的学习排序框架，LTRGR。LTRGR 使生成检索能够直接学习对段落进行排名，通过排名损失优化自回归模型以实现最终的段落排名目标。 该框架仅需要额外的学习排序训练阶段来增强当前的生成检索系统，并且不会给推理阶段增加任何负担。 我们在三个公共基准上进行了实验，结果表明 LTRGR 在生成检索方法中实现了 SOTA 性能。

## 方法
![Alt text](image-1.png)

## 实验
### 实验设置

### 实验结果
![Alt text](image-2.png)


## 相关工作
- Generative Retrieval
- Learning to Rank
- Dense Retrieval