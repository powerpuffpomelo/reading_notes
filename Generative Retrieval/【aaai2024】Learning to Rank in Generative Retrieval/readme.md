# Learning to Rank in Generative Retrieval

论文链接 [Learning to Rank in Generative Retrieval](https://arxiv.org/pdf/2306.15222.pdf)

代码地址 https://github.com/liyongqi67/LTRGR

![Alt text](image.png)

## 动机
- 生成式检索模型的LM学习目标，和 doc排序目标 存在gap。

本文提出一种用于生成式检索的学习排序框架，LTRGR。LTRGR 使生成检索能够直接学习对段落进行排名，通过排名损失优化自回归模型以实现最终的段落排名目标。 该框架仅需要额外的学习排序训练阶段来增强当前的生成检索系统，并且不会给推理阶段增加任何负担。 我们在三个公共基准上进行了实验，结果表明 LTRGR 在生成检索方法中实现了 SOTA 性能。

## 方法
![Alt text](image-1.png)