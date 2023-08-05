# -*- coding: utf-8 -*-
# @Time : 2022/12/28 13:44
# @Author : Zdh
import yaml
import warnings
import argparse

__all__ = ["LoadDefaultOptions", "get_options"]


class LoadDefaultOptions(object):
    def __init__(self, yaml_file):
        super().__init__()
        with open(yaml_file) as f:
            parameters = yaml.load(f, Loader=yaml.FullLoader)
        # 以下为配置文件解析部分
        assert isinstance(parameters, dict), "the option must be an dict data type"
        self.opt = parameters
        self.model = parameters.get("model", None)
        self.dataset = parameters.get("dataset", None)
        self.train = parameters.get("train", None)


def get_options() -> LoadDefaultOptions:
    # TODO 需要最大限度的简化以及自适应加载相关参数
    parser = argparse.ArgumentParser(description='parameters for training')
    parser.add_argument("--config_file", "-opt", type=str, help='配置文件名称')
    args = parser.parse_args()

    assert args.config_file is not None, "you must Specify the configuration file with --opt"
    opt = LoadDefaultOptions(args.config_file)

    return opt







