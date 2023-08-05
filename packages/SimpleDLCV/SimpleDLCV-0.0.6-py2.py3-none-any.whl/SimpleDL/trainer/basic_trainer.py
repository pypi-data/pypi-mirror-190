# -*- coding: utf-8 -*-
# @Time : 2022/12/28 18:12
# @Author : Zdh
from ..utils import get_logger
from ..utils import get_class
from tqdm import tqdm
import torch
import torch.nn as nn
from SimpleDL.utils import AverageValueMeter
from ..model.losses import MixLoss


class BasicTrainer(object):
    def __init__(self, opt):
        super(BasicTrainer, self).__init__()
        self.opt = opt
        self.main_logger = get_logger("SimpleDL")                   # 主日志
        # ******* 必须包含的初始化 ******* #
        device_ids, self.device = self.get_device()
        self.model = get_class(opt=opt["model"])                    # 模型的加载
        if device_ids is not None:
            self.model = nn.DataParallel(self.model, device_ids)
        self.model.to(self.device)
        self.criterion = MixLoss(opt.get("losses", None))
        self.optimizer = get_class(opt=opt["optimizer"], params=self.model.parameters())     # 加载优化器
        self.dataset = get_class(opt=opt["dataset"])                                         # 加载数据集
        self.dataloader = get_class(opt=opt["dataloader"], dataset=self.dataset)             # 加载数据集加载器

        # 可选的初始化
        if opt.get("scheduler", None) is None:
            self.scheduler = None
        else:
            self.scheduler = get_class(opt=opt["scheduler"], optimizer=self.optimizer)
        # 训练过程的一些参数的加载
        self.train_opt = opt.get("train", None)
        self.max_epoch = self.train_opt.get("max_epoch")
        self.img_key = opt["model"]["input_name"]

        # 非配置类加载
        self.metric = AverageValueMeter(ddof=1)
        self.iter_now = 0

    def train(self):
        iter_count = 0
        self.model.train()
        for epoch in range(self.max_epoch):
            tqdm_bar = tqdm(enumerate(self.dataloader), total=len(self.dataloader), desc=f"epoch:{epoch}")
            for ii, data in tqdm_bar:
                # 模型推理与参数更新部分
                img = data[self.img_key].to(self.device)                        # 获得输入图像
                out = self.model(img)                                           # 获得模型输出
                loss_all, loss_recode = self.criterion(out, data)               # 计算损失函数
                self.optimizer.zero_grad()                                      # 清空梯度
                loss_all.backward()                                             # 反向传播
                self.optimizer.step()                                           # 更新模型参数

                # 其他每一iter需要执行的任务
                self.metric.add(loss_all)
                self.iter_now += 1
                self.tqdm_postfix_show(tqdm_bar)                                # 在tqdm上显示一些尾缀提示信息

    def tqdm_postfix_show(self, tqdm_bar, **kwargs):
        postfix_dict = {
            "loss_now": f"{float(self.metric.var()):.5f}",
            "loss_mean": f"{self.metric.mean():.5f}",
        }
        for key, val in kwargs.items():
            postfix_dict[key] = val
        postfix_dict["lr"] = self.optimizer.param_groups[0]["lr"]
        postfix_dict["iter"] = self.iter_now
        tqdm_bar.set_postfix_str(postfix_dict)

    def get_device(self):
        device_ids = []
        msg_info = "used device information:\r\n"
        device_msg = self.opt["train"].get("device", None)

        if isinstance(device_msg, list) or isinstance(device_msg, tuple) and device_msg != []:   # 指定使用GPU
            device_ids = list(device_msg)
            device = f"cuda:{device_ids[0]}"
            for device_id in device_msg:
                cuda_msg = torch.cuda.get_device_properties(device_id)
                msg_info += f"\tuse  cuda:{device_id}-【{cuda_msg.name}】 with {cuda_msg.total_memory / (1 << 20):.0f}MiB\r\n"
            if len(device_ids) == 1:
                device_ids = None
        elif device_msg is not None and device_msg.lower() == "cpu":           # 指定使用cpu
            device_ids = None
            device = "cpu"
            msg_info += "CPU only"
        else:                    # 未指定 则自适应调整
            msg_info = "未指定驱动设备，自适应选择下列设备进行训练：\r\n"
            if torch.cuda.is_available() and torch.cuda.device_count() > 0:
                for device_id in range(torch.cuda.device_count()):
                    device_ids.append(device_id)
                    cuda_msg = torch.cuda.get_device_properties(device_id)
                    msg_info += f"\tuse  cuda:{device_id}-【{cuda_msg.name}】 with {cuda_msg.total_memory / (1 << 20):.0f}MiB\r\n"
                device = f"cuda:{device_ids[0]}"
                if len(device_ids) == 1:
                    device_ids = None
            else:
                device_ids = None
                device = "cpu"
                msg_info += "CPU only"
        self.main_logger.warning(msg_info.strip())
        return device_ids, device




