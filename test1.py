import sys
import os
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

from FCN_U import AlexNet
import data_set


class My_Data(Dataset):
    def __init__(self, data):
        self.data = data[0]

        self.list_data = []
        for i in range(0, len(self.data)):
            self.stem1 = data_set.stem1(self.data[i])
            self.a = data_set.f_dimer(self.stem1, self.data[i])
            # self.a = add_pad(np.array(self.a))
            self.list_data.append(self.a)

    def __getitem__(self, index):
        data = np.array(self.list_data[index])
        data = data.astype(float)
        data = torch.tensor(data)
        data = data.type(torch.FloatTensor)

        # data = data.unsqueeze(3)
        # target = target.unsqueeze(3)
        return data

    def __len__(self):  # 返回所有样本的数目
        return len(self.data)

def out(data):
    data1 = data
    df = pd.DataFrame([data1])

    datatest = My_Data(df)

    test_loader = DataLoader(datatest, shuffle=False)

    np.set_printoptions(threshold=sys.maxsize)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    for a in test_loader:
        data = a
        # print(data.shape)
        data = data.to(device)
        # pretrained_net = VGGNet()
        net = AlexNet()
        net.to(device)
        net.load_state_dict(torch.load(r'trained_model_U_A7.pth', map_location=device))
        net.eval()
        with torch.no_grad():
            output = net(data)
        output = output[0]
        nu_da = output.cpu().numpy()
        nu_da = np.array(nu_da).reshape(nu_da.shape[-1], -1)
        np.savetxt(r'配对概率矩阵2.txt', nu_da, fmt='%f', delimiter=',')
if __name__ == '__main__':
    data = input()
    out(data)
