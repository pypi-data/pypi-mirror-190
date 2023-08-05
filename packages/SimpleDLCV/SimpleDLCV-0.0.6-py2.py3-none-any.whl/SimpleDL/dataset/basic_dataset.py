# -*- coding: utf-8 -*-
# @Time : 2022/12/30 11:47
# @Author : Zdh
from torch.utils.data import dataset
import os
from ..utils import get_class


class BasicDataset(dataset.Dataset):
    def __init__(self, base_path: str, behavior: list, dataset: str = "train", out_size=None, *args, **kwargs):
        """
        :param base_path: str 支持文件或路径，如果是路径则路径中需要保存train.txt val.txt test.txt文件
        文件路径的每一行为一组图像与标签,支持多标签，之间通过空格分隔
        :param dataset: 需要是train test val 三者中的一个
        :param out_size: 图像输出的尺寸，None表示最后的输出不进行尺寸变换（可能需要自定义dataloader的fn）
        """
        super(BasicDataset, self).__init__()
        self.behavior = behavior
        self.base_path = base_path
        self.dataset = dataset
        self.out_size = out_size
        # 读取数据集信息
        if os.path.isfile(self.base_path):
            with open(self.base_path, "r") as f:
                msg_file = f.readlines()
        else:
            with open(os.path.join(self.base_path, F"{dataset.lower()}.txt")) as f:
                msg_file = f.readlines()
        self.msg_file = msg_file

    def __len__(self):
        return len(self.msg_file)

    def __getitem__(self, index):
        item_msg = self.msg_file[index].strip().split(" ")
        output = {}
        for ii, behavior in enumerate(self.behavior):
            out_name = behavior.get("out_name", ii)
            data_id = behavior.get("data_id", 0)
            assert data_id < len(item_msg), "data_id 超出所给info索引范围"
            output[out_name] = get_class(behavior, msg_show=False)(item_msg[data_id])
        return output


