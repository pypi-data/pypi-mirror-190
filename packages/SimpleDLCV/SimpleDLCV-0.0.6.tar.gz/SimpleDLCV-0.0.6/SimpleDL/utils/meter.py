# -*- coding: utf-8 -*-
# @Time : 2023/1/4 14:35
# @Author : Zdh


class AverageValueMeter(object):
    def __init__(self, ddof = 1):
        super(AverageValueMeter, self).__init__()
        self.sum = 0.0
        self.num = 0.0
        self.val = 0.0
        self.var_sum = 0.0
        self.ddof = ddof
        self.__min = None
        self.__max = None

    def add(self, val, num=1):
        self.val = float(val)
        self.sum += self.val
        self.num += num
        self.var_sum += self.val * self.val
        if self.__min is None or self.__min > self.val:
            self.__min = self.val
        if self.__max is None or self.__max < self.val:
            self.__max = self.val
        return self

    def __add__(self, other):
        self.add(other, num=1)
        return self

    def __iadd__(self, other):
        self.add(other, num=1)
        return self

    def mean(self):
        if self.num == 0:
            return float("nan")
        return self.sum / self.num

    def var(self):
        if self.num - self.ddof <= 0:
            return float("nan")
        var = (self.var_sum - 2*self.mean()*self.sum + self.num * self.mean() *self.mean()) / (self.num - self.ddof)
        return var

    def std(self):
        return self.var() ** 0.5

    def min(self):
        return self.__min

    def max(self):
        return self.__max

    def reset(self):
        self.sum = 0.0
        self.num = 0.0
        self.val = 0.0
        self.var_sum = 0.0
        self.__min = None
        self.__max = None

