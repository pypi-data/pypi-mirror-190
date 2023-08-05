# -*- coding: utf-8 -*-
# @Time : 2022/12/28 13:46
# @Author : Zdh
import logging
import warnings
import torch

__all__ = ["logger_init", "get_logger", "get_base_log"]

loggers = []

pro_str ="\033[1;34m                      ,\"                                                       l>>^                                                               \r\n" \
        "  .>(z0wddpZLu:     `OB%v                                                      Z$$]                      ;zXYJJJJUcn\?l'         !XYr.            \r\n" \
        " {d@@pXxtfxzOo+     .}cu+                                                      Z$$]                      <$$$QCCCCQqo8B*J[`      ?$$a'            \r\n" \
        " -$$Wi        .'                     ..        ...                 ...         Z$$]          ...         >B$#`      .:?UB$h{     -$$k'            \r\n" \
        "  _@$8{'             t00_    IL0c\")JqaokC)` ~vmkaodY].     j00<;tQdhoawu_.     Z$$]      :)UphkhbQ\I     >B$#\"          ld$$j    -$$k'            \r\n" \
        "   [p@$#L|<^         Q$$)    <$$%dJ(??(0$$p0#X1-]\d$$J'    O$$qkJ\]-[tw$$wl    Z$$]    ^u&$wt?<-\w$&r.   >B$#\"           ~B$8l   -$$k'            \r\n" \
        "    .>/0#$$&wr<.     C$$1    >B$B}      U$$#!     `h$$_    Q$$dI       \$$d^   Z$$]   `Z$B{       Y$$(   >B$#\"           ,W$$_   -$$k'            \r\n" \
        "        'l{za$$p-    C$$1    >B$h.      \$$Y       Q$${    Q$${        '#$@>   Z$$]   -$$%pdddddddo$$C   >B$#\"           [@$M:   -$$k'            \r\n" \
        "            ')B$%i   C$$1    >B$h'      \$$U       Q$$}    Q$$}        ;&$8I   Z$$]   _$$a?????????__!   >B$#\"          _#$8{    -$$k'            \r\n" \
        "  ;!\'        _B$%i   C$$1    >B$h\'      \$$U       Q$$}    Q$$pl      :O$$n    Z$$]   `m$@/.        .    >B$#`      'I)Z$$Z<     -$$k.            \r\n" \
        "  ($*wJnrrxUp$@p]    Q$$)    <$$o'      /$$J       O$${    Q$$bo0x||r08$h(     w$$[    \"z&$oUf)1/nQa)    <$$$QCCCQmd*%%kv<       ?$$BLCCCCCCCC<   \r\n" \
        "  \"{rY0mwwZLv)!.     )zz<    :vzj.      +zz{       (zzi    Q$$[ltCZmmCr_\'      |zc!      :}uQmmmOJx[\"    :vczYYYYXuf1~:          lcczYYYYYYYYY<   \r\n" \
        "                                                           Q$$}                                                                                   \r\n" \
        "                                                           0$${                                                                                   \r\n" \
        "                                                           chh?                                                                                   \r\n" \
        "                                                           .\'\'.                                                                                   \r\n" \
        "Information:\r\n" \
        "  SimpleDLCV vesion: 1.0.0\r\n" \
        f"  Pytorch vesion : {torch.__version__}\r\n" \
        f"  CUDA vesion    ：{torch.version.cuda}\r\n" \
        f"power by SimpleDLCV: \033[0m"                                   # TODO:git 地址


# 日志的色彩实现方式
class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, color_config=None):
        super(ColoredFormatter, self).__init__()
        logging.Formatter.__init__(self, msg)
        self.color_config = color_config
        self.color = {"black": "30", "red": "31", "green": "32", "yellow": "33", "blue": "34", "fuchsia": "35", "cyan": "36", "white": "37"}

    def format(self, record):
        levelname = record.levelname
        color_prefix = ""
        color_suffix = ""
        if self.color_config is not None and levelname in self.color_config.keys():
            # 检查是否支持此颜色
            used_color = self.color_config[levelname].lower()
            if used_color not in self.color.keys():
                warnings.warn(f"{self.color_config[levelname]} is not support, you can use color in {self.color.keys()}")
            else:
                color_prefix = f"\033[0;{self.color[used_color]}m"
                color_suffix = "\033[0m"
        return color_prefix + logging.Formatter.format(self, record) + color_suffix


def logger_init(name: str, save_file=None):
    logger = logging.getLogger(name)
    if name in loggers:                 # 避免重复的初始化
        return logger
    logger.setLevel(logging.DEBUG)          # 默认的最低输出等级
    log_colors_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }
    color_log_format = ColoredFormatter("[%(asctime)s] %(filename)s-line:%(lineno)d [%(levelname)s] : %(message)s", log_colors_config)
    default_log_format = ColoredFormatter("[%(asctime)s] %(filename)s-line:%(lineno)d [%(levelname)s] : %(message)s")

    # stream输出部分
    log_stream = logging.StreamHandler()
    log_stream.setLevel(logging.INFO)
    log_stream.setFormatter(color_log_format)       # 使用带颜色的日志输出，为了醒目warning
    logger.addHandler(log_stream)
    # file 输出部分
    if save_file is not None:
        log_file = logging.FileHandler(save_file, 'w+')
        log_file.setLevel(logging.DEBUG)
        log_file.setFormatter(default_log_format)
        logger.addHandler(log_file)

    loggers.append(name)

    print(pro_str)

    return get_logger(name)


def get_logger(name: str):
    assert name in loggers, f"You must initialize the {name}_logger before using"
    return logging.getLogger(name)


def get_base_log():
    return get_logger("SimpleDLCV")
