# Alpaca: A Strong, Replicable Instruction-Following Model

博客链接 [Alpaca: A Strong, Replicable Instruction-Following Model](https://crfm.stanford.edu/2023/03/13/alpaca.html)

github [Stanford Alpaca: An Instruction-following LLaMA Model](https://github.com/tatsu-lab/stanford_alpaca)

Alpaca 的来源是 Meta 公司发布的 LLaMA 7B 模型。

斯坦福的研究团队在 LLaMA 7B 模型的基础上，进行了进一步的微调，使其能够执行指令。他们使用了 OpenAI 的 text-davinci-003 模型，它是一个基于 GPT-3.5 的指令执行模型，来生成 52K 条指令执行的示例数据。这些数据包括了不同类型和难度的指令，例如：

- 写一首关于春天的诗。
- 写一个 Python 程序，计算两个数的最大公约数。
- 写一个关于狼人杀游戏规则的简介。

然后，他们使用了 Self-Instruct 的方法，来对 LLaMA 7B 模型进行微调。Self-Instruct 是一种基于自我监督的方法，它可以利用指令执行模型自身生成的数据来进行训练。具体来说，Self-Instruct 的流程如下：

- 首先，给定一个预训练好的语言模型 fθ 和一个指令 x 。
- 然后，使用 fθ 来生成一个指令执行结果 y 。
- 接着，使用 fθ 来生成一个对结果 y 的评价 z 。
- 最后，使用 ( x, y, z ) 作为训练样本，来更新模型参数 θ 。

通过这种方式，Self-Instruct 可以利用语言模型自身生成高质量且多样化的指令执行数据来进行训练。

经过微调后，斯坦福的研究团队得到了 Alpaca 7B 模型，它是一个基于指令执行的语言模型，可以根据用户给出的指令，生成不同类型的文本内容。