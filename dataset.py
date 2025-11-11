import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import data_set


'''def add_pad(data):
    data = data
    shape = data.shape

    if shape[1] < 32:
        pad_a = float((32 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((33 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))
    if (shape[1] > 32) and (shape[1] < 64):
        pad_a = float((64 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((65 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))
    if (shape[1] > 64) and (shape[1] < 128):
        pad_a = float((128 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        # print(type(int(n)))
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((129 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))
    if (shape[1] > 128) and (shape[1] < 256):
        pad_a = float((256 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((257 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))

    if (shape[1] > 256) and (shape[1] < 512):
        pad_a = float((512 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((513 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))

    if (shape[1] > 512) and (shape[1] < 1024):
        pad_a = float((1024 - shape[1]) / 2)
        n = list(str(pad_a).split('.'))[1]
        if int(n) == 0:
            pad_a = int(pad_a)
            data = np.pad(data, ((0, 0), (pad_a, pad_a), (pad_a, pad_a)))
        if int(n) != 0:
            pad_a = float((1025 - shape[1]) / 2)
            pad_a = int(pad_a)
            pad_b = pad_a - 1
            data = np.pad(data, ((0, 0), (pad_a, pad_b), (pad_b, pad_a)))
    return data
'''

class MyData(Dataset):
    def __init__(self, path):
        self.datapath = path
        self.data_all = pd.read_csv(self.datapath, header=None)
        self.data = self.data_all.iloc[:, 0]
        self.target = self.data_all.iloc[:, 1]
        self.list_data = []
        self.list_target = []
        for i in range(0, len(self.data)):
            self.stem1 = data_set.stem1(self.data[i])
            self.a = data_set.f_dimer(self.stem1, self.data[i])
            self.list_data.append(self.a)
            print("第"+ str(i))
        for j in range(0, len(self.target)):

            self.b = data_set.target(self.target[j])
            self.list_target.append(self.b)

    def __getitem__(self, index):
        data = np.array(self.list_data[index])
        target = np.array(self.list_target[index])

        data = data.astype(float)
        target = target.astype(float)
        data = torch.tensor(data)
        target = torch.tensor(target)
        data = data.type(torch.FloatTensor)
        target = target.type(torch.FloatTensor)
        # data = data.unsqueeze(3)
        # target = target.unsqueeze(3)
        return data, target

    def __len__(self):  # 返回所有样本的数目
        return len(self.data)


dataset = MyData("data/RNAStructure_Train.csv")

train_size = int(len(dataset) * 0.8)
test_size = len(dataset) - train_size

train_loader = DataLoader(dataset,shuffle=False)


