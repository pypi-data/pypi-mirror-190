# -*- coding: utf-8 -*-
# @Time : 2022/12/28 10:56
# @Author : Zdh
from .logger import *
from importlib import import_module
from .meter import AverageValueMeter


def get_class(opt, msg_show=True, **kwargs):
    """
    :param opt: 包含类和初始参数的配置文件
    :param kwargs: 额外需要传递的参数
    :return:
    """
    class_type = opt.get("type", None)
    class_split = class_type.split(".")
    package_name = ".".join(class_split[:-1])
    class_name = class_split[-1]
    args = opt.get("args", None)
    for key, value in list(kwargs.items()):
        args[key] = value
    assert class_type and package_name and class_name and args is not None, "options must be like " \
                    "{type:{package: Model.layer,class: resnet,},args: {your args dict}"
    obj = getattr(import_module(package_name), class_name)(**args)

    if msg_show:
        if args == {}:
            info_msg = f"[{class_name}]初始化成功"
        else:
            info_msg = f"[{class_name}]初始化成功-("
            for key, value in list(args.items()):
                info_msg += f"{key}:{value}, "
            info_msg += ")"
        get_base_log().info(info_msg)
    return obj
