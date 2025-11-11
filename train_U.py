import os
import torch
from torch import optim, nn

import matplotlib.pyplot as plt

from FCN_U import AlexNet #FCN_Net,
from dataset import MyData, train_loader
import torchvision.models as models

os.environ['TORCH_HOME'] = r"C:/Users/lenovo/Desktop/FCN_AL"
def train_model(model, criterion, device, optimizer, traindataloader, num_epochs):
    """
    model：训练模型，
    criterion：损失函数，
    optimizer：优化方法，
    traindataloader：训练数据集，
    valdataloader：验证数据集，
    num_epochs：训练轮数
    """

    train_loss_all = []  # 损失函数总和，随时更新

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)
        train_loss = 0.0
        train_num = 0

        # 每个epoch包括训练和验证阶段

        for step, (b_x, b_y) in enumerate(traindataloader):
            # b_x = torch.squeeze(b_x)
            # b_y = torch.squeeze(b_y)
            b_x = b_x.to(device, dtype=torch.float32)  # 将数据放入GPU训练
            b_y = b_y.to(device, dtype=torch.float32)
            model.train()  # 设置模型为训练模式
            out = model(b_x)  # 通过模型计算后的输出

            loss = criterion(out, b_y)  # 计算损失函数值
            optimizer.zero_grad()
            loss.backward()  # 反向传播
            optimizer.step()  # 更新参数
            train_loss += loss.item() * len(b_y)
            train_num += len(b_y)
            # 计算一个epoch训练后在验证集上的损失

        train_loss_all.append(train_loss / train_num)
        print('{} Train loss: {:.4f}'.format(epoch, train_loss_all[-1]))
    plt.switch_backend('Agg')
    # 1.训练时先新建个列表，然后将loss值调用列表的append方法存入列表中
    # 2.例如列表train_recon_loss，Discriminator_loss...，然后将列表名替换train_recon_loss，Discriminator，利用plot即可画出曲线
    # 3.最后将画的图保存成图片，imgpath为自定义的图片保存路径。
    # plt.figure(num = 2, figsize=(640,480))
    imgPath = 'C:/Users/lenovo/Desktop/FCN_AL/code'
    plt.figure()
    plt.plot(train_loss_all, 'b', label='Recon_loss')
    plt.ylabel('Recon_loss')
    plt.xlabel('iter_num')
    plt.legend()
    plt.savefig(os.path.join(imgPath, "A3_U_recon_loss.jpg"))  # 画损失函数图像

    torch.save(model.state_dict(), r'C:/Users/lenovo/Desktop/FCN_AL/code/trained_model_U_A5.pth')  # 保存训练好的模型

    return model


if __name__ == '__main__':
    #dataset = MyData("D:/FCN_RNA/data_demo.csv")

    '''`
    train_dataset：训练数据集
    validate_dataset：验证数据集
    test_dataset：测试数据集'''

    train_loader = train_loader

    model = AlexNet()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 使用GPU训练
    model = model.to(device)  # 将模型载入GPU训练



    optimizer = optim.Adam(params=model.parameters(), lr=0.001)  # 使用Adam优化器，学习率为0.001
    criterion = nn.MSELoss()  # 损失函数为均方误差损失函数
    num_epoch = 20  # 训练两轮
    train = train_model(model, criterion, device, optimizer, train_loader,
                        num_epoch)  # 开始训练，传入：模型，损失函数，GPU训练，优化器，训练集，训练轮数这六个参数
