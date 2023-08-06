# -*- coding: UTF-8 -*-
"""
@Project :FedDCM @File :server.py
@IDE :PyCharm @Author : hejunshu
@Date :2022/9/28 10:09
"""
import numpy as np
import math
from FedDCM1.client_matrix import SMWTPClientMatrix
from FedDCM1.client_single import SMWTPClientSingle
from FedDCM1.dcm import SMWillingToPay


class Server:
    def __init__(self, mode,
                 len_burn_in, len_draw, len_skip, rho, accept_rate,
                 mean_coeff_var, inter_coeff_var, inter_covar, num_attrib_var, num_people,
                 draws_mean_var, draws_inter_coeff_var, draws_inter_covar,
                 clients=list, client_matrix=classmethod
                 ):
        self.mode = mode
        self.client_matrix = client_matrix
        self.clients = clients

        self.len_burn_in = len_burn_in
        self.len_draw = len_draw
        self.len_skip = len_skip
        self.iterations = self.len_burn_in + self.len_draw * self.len_skip
        self.rho = rho
        self.accept_rate = accept_rate

        self.mean_coeff_var = mean_coeff_var
        self.inter_coeff_var = inter_coeff_var
        self.inter_covar = inter_covar

        self.draws_mean_var = draws_mean_var
        self.draws_inter_coeff_var = draws_inter_coeff_var
        self.draws_inter_covar = draws_inter_covar

        self.num_attrib_var = num_attrib_var
        self.num_people = num_people

    def InterDrawMeans(self):
        temp1 = (np.mean(self.inter_coeff_var, 1)).reshape(self.num_attrib_var, 1)
        normal = np.random.multivariate_normal(np.zeros(self.num_attrib_var), np.identity(self.num_attrib_var),
                                               size=1).T
        temp2 = np.dot(np.linalg.cholesky(self.inter_covar / self.num_people), normal)
        self.mean_coeff_var = temp1 + temp2

    def AggPopMeans(self):
        self.mean_coeff_var = np.mean(self.inter_coeff_var, 1).reshape(self.num_attrib_var, 1)  # 5位一维数组 1*5

    def InterDrawCovar(self):
        temp1 = self.inter_coeff_var - np.tile(self.mean_coeff_var, (1, self.num_people))  # 5*100
        temp2 = np.dot(temp1, temp1.T) + self.num_attrib_var * np.identity(self.num_attrib_var)  # indentity 单位矩阵
        temp3 = np.linalg.cholesky(np.linalg.inv(temp2))  # 5*5 inv 求逆
        normal = np.random.multivariate_normal(np.zeros(self.num_attrib_var), np.identity(self.num_attrib_var),
                                               size=(self.num_people + self.num_attrib_var)).T
        temp4 = np.dot(temp3, normal)
        self.inter_covar = np.linalg.inv(np.dot(temp4, temp4.T))

    def AggInterCovar(self):
        temp1 = self.inter_coeff_var - np.tile(self.mean_coeff_var, (1, self.num_people))  # 5*100
        self.inter_covar = np.dot(temp1, temp1.T) / self.num_people

    def sync_training_matrix(self):
        for i in range(self.iterations):
            self.client_matrix.refresh(self.mean_coeff_var, self.inter_covar, self.rho)
            self.inter_coeff_var, is_draw = self.client_matrix.InterDrawCoeffMatrix()
            if self.mode == '_SPL':
                self.InterDrawMeans()
                self.InterDrawCovar()
            if self.mode == '_AGG':
                self.AggPopMeans()
                self.AggInterCovar()
            draw_rate = np.sum(is_draw) / self.num_people
            self.rho = self.rho - 0.1 * self.rho * (draw_rate < self.accept_rate) + 0.1 * self.rho * (
                    draw_rate > self.accept_rate)

    def sync_training_single(self):
        id_train = list(range(len(self.clients)))
        for i in range(self.iterations):
            inter_coeff_var = []
            num_draw = 0
            for id, j in enumerate(id_train):
                self.clients[j].refresh(self.mean_coeff_var, self.inter_covar, self.rho)
                coeff_var_j, is_draw = self.clients[j].InterDrawCoeff()
                inter_coeff_var.append(coeff_var_j.reshape(self.num_attrib_var))
                num_draw += sum(is_draw)
            self.inter_coeff_var = np.swapaxes(np.array(inter_coeff_var), 0, 1)
            draw_rate = num_draw / self.num_people
            self.rho = self.rho - 0.1 * self.rho * (draw_rate < self.accept_rate) + 0.1 * self.rho * (
                    draw_rate > self.accept_rate)
            if self.mode == '_SPL':
                self.InterDrawMeans()
                self.InterDrawCovar()
            if self.mode == '_AGG':
                self.AggPopMeans()
                self.AggInterCovar()


class SMWTPServer(Server):
    def __init__(self, mode, filepath, filename,
                 len_burn_in, len_draw, len_skip, rho, accept_rate,
                 cmp_mode='_Matrix'
                 ):
        model = SMWillingToPay(filepath, filename)

        num_attrib_var = model.num_attrib_var
        num_people = model.num_people

        mean_ori = np.array([[0], [0], [0], [0]])
        mean_coeff_var = mean_ori
        inter_coeff_var = np.ones((num_attrib_var, num_people))
        inter_coeff_var = mean_coeff_var * inter_coeff_var
        inter_covar = num_attrib_var * np.identity(num_attrib_var)

        draws_mean_var = np.zeros((num_attrib_var, len_draw))
        draws_inter_coeff_var = np.zeros((num_attrib_var, num_people, len_draw))
        draws_inter_covar = np.zeros((num_attrib_var, num_attrib_var, len_draw))

        self.cmp_mode = cmp_mode
        if self.cmp_mode == '_Single':
            clients = []
            for i in range(num_people):
                clients.append(SMWTPClientSingle(i, model, mean_coeff_var, inter_covar, mean_coeff_var, rho))

            Server.__init__(self, mode, len_burn_in, len_draw, len_skip, rho, accept_rate, mean_coeff_var,
                            inter_coeff_var, inter_covar, num_attrib_var, num_people, draws_mean_var,
                            draws_inter_coeff_var,
                            draws_inter_covar, clients=clients)
        else:
            Clients_Matrix = SMWTPClientMatrix(model, mean_coeff_var, inter_covar, inter_coeff_var, rho)
            Server.__init__(self, mode, len_burn_in, len_draw, len_skip, rho, accept_rate, mean_coeff_var,
                            inter_coeff_var, inter_covar, num_attrib_var, num_people, draws_mean_var, draws_inter_coeff_var,
                            draws_inter_covar, client_matrix=Clients_Matrix)


















