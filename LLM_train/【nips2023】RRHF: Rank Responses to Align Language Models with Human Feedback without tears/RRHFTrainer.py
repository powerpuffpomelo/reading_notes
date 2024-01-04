import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Sequence
import io
import torch
import torch.nn.functional as F
import transformers
from torch.utils.data import Dataset
from transformers import Trainer
import json

class RRHFTrainer(Trainer):
    def gather_logits_labels(self, logits, labels):
        """
        从预测的logit中收集真实标签对应位置的logit，同时忽略那些被标记为-100的位置。
        输出: [bsz, seq_len]
        """
        mask = (labels != -100).float()
        new_logits = logits.clone()  # Create a copy to avoid in-place modification
        labels[labels == -100] = 0 
        output = torch.gather(new_logits, dim=-1, index=labels.unsqueeze(-1)).squeeze(-1)
        output = output * mask # B * L
        return output

    def get_score(self, logit_label, labels):
        """
        长度归一化，得到每个seq的解码概率分数
        输出: [bsz]
        """
        mask = (labels != -100).float()
        length = mask.sum(-1)
        scores = logit_label.sum(-1) / (length ** self.args.length_penalty)
        return scores

    def rrhf_loss(self, scores, idxs, rw_scores):
        """
        首先，计算scores（前一个函数get_score的输出，也就是每个序列的得分）之间的差异，得到一个形状为b * b的矩阵diff，其中b是batch size。
        然后，计算rw_scores（真实的排名得分）之间的差异，得到一个形状为b * b的矩阵rw_diff。
        接着，计算一个aval矩阵，其中的元素为True当且仅当对应的rw_diff大于0且diff小于0。也就是说，aval矩阵标记了那些模型预测的排名低于真实排名的位置。
        最后，将aval矩阵中对应位置的diff的和取负数，得到最终的损失值。这个损失值反映了模型预测的排名低于真实排名的程度，模型的目标是最小化这个损失值。
        """
        diff = scores.unsqueeze(0) - scores.unsqueeze(-1) # b * b
        rw_diff = rw_scores.unsqueeze(0) - rw_scores.unsqueeze(-1) # b * b
        aval = torch.bitwise_and(rw_diff > 0, diff < 0)[0]
        return -diff[aval].sum()

    def sft_loss(self, logit_label, idxs, rw_scores):
        """
        取reward分数最高的位置的log
        """
        max_idx = torch.argmax(rw_scores)
        return -logit_label[max_idx].mean()

    def compute_loss(self, model, inputs, return_outputs=False):
        if self.args.only_use_provide:
            inputs['input_ids'] = inputs['input_ids'][-2:]
            inputs['attention_mask'] = inputs['attention_mask'][-2:]
            inputs['labels'] = inputs['labels'][-2:]
            inputs["idxs"] = inputs["idxs"][:,-2:]
            inputs["scores"] = inputs["scores"][:,-2:]
        if self.args.only_use_sample:
            inputs['input_ids'] = inputs['input_ids'][:-2]
            inputs['attention_mask'] = inputs['attention_mask'][:-2]
            inputs['labels'] = inputs['labels'][:-2]
            inputs["idxs"] = inputs["idxs"][:,:-2]
            inputs["scores"] = inputs["scores"][:,:-2]
        logits = model(input_ids=inputs.get('input_ids'), attention_mask=inputs.get('attention_mask'))[0] # (batch * cand) * L * V
        logits = F.log_softmax(logits, dim=-1)
        logit_label = self.gather_logits_labels(logits, inputs.get("labels"))
        scores = self.get_score(logit_label, inputs.get("labels"))
        rrhf_loss = self.rrhf_loss(scores, inputs.get("idxs"), inputs.get("scores"))
        sft_loss = self.sft_loss(logit_label, inputs.get("idxs"), inputs.get("scores"))
        loss = self.args.rrhf_weight * rrhf_loss + sft_loss
        return (loss, scores) if return_outputs else loss
        