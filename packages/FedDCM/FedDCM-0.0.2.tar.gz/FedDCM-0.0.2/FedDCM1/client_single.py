# -*- coding: UTF-8 -*-
"""
@Project :FedDCM @File :client.py
@IDE :PyCharm @Author : hejunshu
@Date :2022/9/28 10:09
"""
import numpy as np
import math



class ClientSingle:
    def __init__(self, index, mean_coeff_var, inter_covar, inter_coeff_var, rho,
                 num_attrib_var, num_attrib_fix, attrib_var_tag,
                 num_alter, num_train_menu, num_test_menu, num_attrib_var_data,
                 coeff_fix, train_var, train_fix, test_var, test_fix):
        self.id = index
        self.attrib_var_tag = attrib_var_tag
        self.num_attrib_var = num_attrib_var
        self.num_attrib_var_data = num_attrib_var_data
        self.num_attrib_fix = num_attrib_fix
        self.num_alter = num_alter

        self.num_train_menu = num_train_menu
        self.num_test_menu = num_test_menu

        self.coeff_fix = coeff_fix
        self.mean_coeff_var = mean_coeff_var
        self.inter_covar = inter_covar
        self.inter_coeff_var = inter_coeff_var  # 1* num_attrib_var

        self.rho = rho

        self.train_var = train_var  # num_alter, num_per_menu, num_attrib_var_data
        self.train_fix = train_fix
        self.test_var = test_var
        self.test_fix = test_fix
        self.inter_p = self.InterProb(self.InterTransNormals(self.inter_coeff_var), self.train_fix, self.train_var,
                                      self.num_train_menu)

    def InterDrawCoeff(self):
        # try:
        #     temp1 = np.linalg.cholesky(self.inter_covar)
        # except np.linalg.LinAlgError:
        #     temp1 = nearestPD(self.inter_covar)

        temp1 = np.linalg.cholesky(self.inter_covar)
        temp2 = np.random.randn(self.num_attrib_var, 1)
        temp3 = math.sqrt(self.rho) * np.dot(temp1, temp2)
        inter_coeff_new = self.inter_coeff_var + temp3
        bn = inter_coeff_new - self.mean_coeff_var
        bo = self.inter_coeff_var - self.mean_coeff_var
        p_new = self.InterProb(self.InterTransNormals(inter_coeff_new), self.train_fix, self.train_var,
                               self.num_train_menu)

        temp1 = p_new / self.inter_p
        temp2 = np.dot(np.linalg.inv(self.inter_covar), bn)  # 4*1
        temp3 = np.dot(np.linalg.inv(self.inter_covar), bo)
        temp3 = np.exp(-0.5 * (np.sum(bn * temp2, axis=0) - np.sum(bo * temp3, axis=0)))
        r = temp1 * temp3

        is_draw = np.random.rand(1) <= r
        self.inter_p = p_new * is_draw + self.inter_p * (1 - is_draw)
        self.inter_coeff_var = inter_coeff_new * is_draw + self.inter_coeff_var * (1 - is_draw)
        return self.inter_coeff_var, is_draw

    def InterProb(self, coeff_var_temp, x_fix, x_var, num_menu, scale=1):
        coeff_var = coeff_var_temp.copy()

        if self.num_attrib_fix > 0:
            f = self.coeff_fix.reshape(1, 1, self.num_attrib_fix)
            f = np.tile(f, (self.num_alter, num_menu, 1))
            u = np.sum(f * x_fix, 2)  # num_alter, num_per_menu
            u = u.reshape(self.num_alter, num_menu)
        else:
            u = np.zeros((self.num_alter, num_menu))

        if self.num_attrib_var > 0:
            v = coeff_var[0:self.num_attrib_var_data].reshape(1, 1, self.num_attrib_var_data)
            v = np.tile(v, (self.num_alter, num_menu, 1))
            temp = np.sum(v * x_var, 2)
            u += temp.reshape(self.num_alter, num_menu)

        if scale:
            scale = coeff_var[-1].reshape(1, 1)
            scale = np.tile(scale, (self.num_alter, num_menu))
            u = u / scale

        u_max = np.max(u, 0).reshape(1, num_menu)
        u_max = np.tile(u_max, (self.num_alter, 1))
        u_div = u - u_max
        u_div = np.exp(u_div)
        u_div_label = u_div[-1, :]
        p = u_div_label / np.sum(u_div, 0)
        p = np.prod(p, axis=0)
        if np.isnan(p):
            p = 0
        return p

    def InterTransNormals(self, coeff):
        var_trans = coeff.copy()
        var_trans[self.attrib_var_tag[:, 1] == 2, :] = np.exp(var_trans[self.attrib_var_tag[:, 1] == 2, :])
        return var_trans

    def refresh(self, mean_coeff_var, inter_covar, rho):
        self.mean_coeff_var = mean_coeff_var
        self.inter_covar = inter_covar
        self.rho = rho


class SMWTPClientSingle(ClientSingle):
    def __init__(self, index, model,
                 mean_coeff_var, inter_covar, inter_coeff_var, rho):
        ClientSingle.__init__(self, index, mean_coeff_var, inter_covar, inter_coeff_var, rho,
                              model.num_attrib_var, model.num_attrib_fix, model.attrib_var_tag,
                              model.num_alter, model.num_train_menu, model.num_test_menu, model.num_attrib_var_data,
                              model.coeff_fix,
                              model.train_var[:, :, :, index], model.train_fix[:, :, :, index],
                              model.test_var[:, :, :, index], model.test_fix[:, :, :, index])

