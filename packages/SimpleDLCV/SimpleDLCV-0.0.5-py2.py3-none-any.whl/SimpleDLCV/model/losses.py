# -*- coding: utf-8 -*-
# @Time : 2023/1/4 17:56
# @Author : Zdh
import torch
import torch.nn as nn
from ..utils import get_class


class MixLoss(nn.Module):
    def __init__(self, opt):
        super(MixLoss, self).__init__()
        self.opt = opt
        self.loss_list = []
        for loss_msg in opt:
            recode_dict = {
                "loss_fn": get_class(loss_msg),
                "model_out_idx": loss_msg["model_out_idx"],
                "label_key": loss_msg["label_key"],
                "weight": loss_msg["weight"],
                "name": loss_msg["name"]
            }
            self.loss_list.append(recode_dict)

    def forward(self, model_out, label):
        loss_all = None
        loss_recode = {}
        if isinstance(model_out, torch.Tensor):
            model_out = [model_out]
        for ii, loss_msg in enumerate(self.loss_list):
            loss_fn = loss_msg["loss_fn"]
            model_out_idx = loss_msg["model_out_idx"]
            label_key = loss_msg["label_key"]
            weight = loss_msg["weight"]
            name = loss_msg["name"]
            device = model_out[model_out_idx].device
            temp_loss = weight * loss_fn(model_out[model_out_idx], label[label_key].to(device))
            if ii == 0:
                loss_all = temp_loss
            else:
                loss_all += temp_loss
            loss_recode[name] = temp_loss
        return loss_all, loss_recode


