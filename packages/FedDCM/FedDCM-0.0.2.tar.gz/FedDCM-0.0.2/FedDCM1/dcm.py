# -*- coding: UTF-8 -*-
"""
@Project :FedDCM @File :dcm.py
@IDE :PyCharm @Author : hejunshu 
@Date :2022/9/28 11:03
"""
import numpy as np


class SMWillingToPay:
    # 存储数据以及对应的DCM结构   数据参数  模型参数
    def __init__(self, filepath, filename):
        super(SMWillingToPay, self).__init__()
        # 数据特征
        self.attrib_var_tag = np.array([[3, 2], [5, 1], [6, 1], [-1, 2]])  # 1：normal 2：log-normal 最后一项放scale factor -1 代表空值
        self.num_attrib_var = self.attrib_var_tag.shape[0]

        self.num_attrib_var_data = self.num_attrib_var - 1  # 减去scale
        self.names_attrib_var = np.array([['TIME'], ['isCAR'], ['isSM'], ['SCALING']])
        self.attrib_fix_tag = np.array([[4]])  # 对应data里面的索引
        self.num_attrib_fix = self.attrib_fix_tag.shape[0]
        self.names_attrib_fix = np.array(['COST'])
        self.coeff_fix = np.array([1])

        # 模型特征
        self.fixed_para = 100
        self.num_alter = 3  # 每次面临的选择数
        self.num_per_menu = 9  # 每个人保有的menu数量
        self.num_train_menu = 8
        self.num_test_menu = self.num_per_menu - self.num_train_menu

        # 加载和预处理sm数据
        data_name = filepath + filename + '.csv'
        data = np.loadtxt(data_name, skiprows=1, delimiter=",")
        data[:, 3:5] = - data[:, 3:5]  # 让price前的系数为-1
        data[:, 3:5] = data[:, 3:5] / self.fixed_para

        # 获取模型参数
        self.num_people = int(len(data) / self.num_alter / self.num_per_menu)

        # 将数据处理为运算结构
        ID = data[:, 0]
        x_var = np.zeros((self.num_alter, self.num_per_menu, self.num_attrib_var_data, self.num_people))
        x_fix = np.zeros((self.num_alter, self.num_per_menu, self.num_attrib_fix, self.num_people))

        for i in range(self.num_people):
            choi_situ = data[ID == i, 1]
            alter = data[ID == i, 2]
            attrib_var = data[ID == i, self.attrib_var_tag[0:self.num_attrib_var_data, [0]]].T
            attrib_fix = data[ID == i, self.attrib_fix_tag[:, [0]]].T
            for t in range(self.num_per_menu):
                k = sum(choi_situ == t) - 1  # 2 number of non chosen alts
                if self.num_attrib_var > 0:
                    x_var[0:k, t, :, i] = attrib_var[(choi_situ == t) & (alter == 0), :]
                    x_var[-1, t, :, i] = attrib_var[(choi_situ == t) & (alter == 1), :]
                if self.num_attrib_fix > 0:
                    x_fix[0:k, t, :, i] = attrib_fix[(choi_situ== t) & (alter == 0), :]
                    x_fix[-1, t, :, i] = attrib_fix[(choi_situ == t) & (alter == 1), :]

        self.train_var = x_var[:, 0:self.num_train_menu, :, :]
        self.train_fix = x_fix[:, 0:self.num_train_menu, :, :]
        self.test_var = x_var[:, self.num_train_menu:self.num_per_menu, :, :]
        self.test_fix = x_fix[:, self.num_train_menu:self.num_per_menu, :, :]



