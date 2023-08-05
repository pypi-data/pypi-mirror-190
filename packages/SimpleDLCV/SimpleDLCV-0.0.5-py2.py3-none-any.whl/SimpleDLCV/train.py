# -*- coding: utf-8 -*-
# @Time : 2022/12/28 16:57
# @Author : Zdh
from .option import get_options
from .trainer import BasicTrainer
from .utils import *
import os

__all__ = ["train_pipline"]


def parameter_check(opt, root_path):
    """
    :param root_path:
    :param opt:
    :return:
    """
    part_info_str = []
    # 必须配置的检查
    if opt.get("model", None) is None:
        raise KeyError("必须实现model配置")
    if opt.get("optimizer", None) is None:
        raise KeyError("必须实现optimizer配置")
    # 全局配置检查
    if opt.get("global", None) is None:
        opt["global"] = {}
        part_info_str.append("配置文件 global 关键字不存在，自动进行创建")
    if opt["global"].get("name", None) is None:
        opt["global"]["name"] = "default"
        global_name = opt["global"]["name"]
        part_info_str.append(f"global配置 name 关键字不存在，自动进行创建[{global_name}]")
    pro_name = opt["global"]["name"]

    # 调度器配置检查
    if opt.get("scheduler", None) is None:
        part_info_str.append("scheduler未定义，推荐使用调度器以获取更优的训练参数")
    # 保存路径的检查
    if opt.get("save", None) is None:
        part_info_str.append("配置文件 save 关键字不存在，自动进行创建")
        opt["save"] = {}
    if opt["save"].get("save_path", None) is None:
        save_path = os.path.join(root_path, f"Checkpoint/{pro_name}")
        opt["save"]["save_path"] = save_path
        part_info_str.append(f"save_path 使用默认配置[{save_path}]")
    save_path = opt["save"]["save_path"]
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if opt["save"].get("logger_path", None) is None:
        logger_path = os.path.join(save_path, "run.log")               # TODO：需要更准确的日志名称
        opt["save"]["logger_path"] = logger_path
        part_info_str.append(f"logger_path 使用默认配置[{logger_path}]")
    # model的input_name 检查
    if opt["model"].get("input_name", None) is None:
        opt["model"]["input_name"] = "img"
        part_info_str.append("model的input_name未定义，使用默认值'img'")
    return opt, part_info_str


def train_pipline(root_path):
    opt = get_options().opt
    opt, check_info = parameter_check(opt, root_path)                   # 一些参数检查
    logger = logger_init("SimpleDLCV", opt["save"]["logger_path"])        # 初始化logger
    for info in check_info:                                             # 输出参数检查信息
        logger.warning(info)
    BasicTrainer(opt).train()



