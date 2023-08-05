# -*- coding: utf-8 -*-
# @Time : 2023/1/3 13:24
# @Author : Zdh
import torch
from PIL import Image

__all__ = ["MinMaxScaler", "PILImageToRGB"]


class MinMaxScaler(object):
    def __init__(self, min, max):
        super().__init__()
        self.max = max
        self.min = min

    def __call__(self, img: torch.Tensor):
        img = (img - self.min) / (self.max - self.min)
        return img


class PILImageToRGB(object):
    def __init__(self):
        super(PILImageToRGB, self).__init__()

    def __call__(self, img):
        img = img.convert("RGB")
        return img

