# -*- coding: utf-8 -*-
# @Time : 2022/12/30 16:07
# @Author : Zdh
from PIL import Image
from torchvision.transforms import transforms as T
from ..utils import get_class
import torchvision.transforms as T

__all__ = ["LoadImageBehavior", "ClassifiBehavior"]

class BasicBehavior(object):
    def __init__(self):
        super(BasicBehavior, self).__init__()

    def __call__(self, msg):
        raise NotImplementedError("需要定义用于处理信息的__call__函数")


class LoadImageBehavior(BasicBehavior):
    def __init__(self, transforms):
        super(LoadImageBehavior, self).__init__()
        self.transforms = transforms

    def __call__(self, msg):
        msg_info = ""
        img = Image.open(msg)
        # 数据增强部分
        transforms_list = []
        for transform in self.transforms:
            transforms_list.append(get_class(transform, msg_show=False))
        transforms = T.Compose(transforms_list)
        img = transforms(img)
        return img


class ClassifiBehavior(BasicBehavior):
    def __init__(self):
        super(ClassifiBehavior, self).__init__()

    def __call__(self, msg):
        return int(msg)

