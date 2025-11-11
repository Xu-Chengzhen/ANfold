import torch
from torch import nn
from torchsummary import summary
import torch.nn.functional as F

CH_FOLD2 = 1
groups = 1
class conv_block1(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_block1, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.GroupNorm(groups,ch_out),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.conv(x)
        return x


class conv_block2(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_block2, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.GroupNorm(groups,ch_out),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.conv(x)
        return x


class conv_block3(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_block3, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.GroupNorm(groups,ch_out),
            nn.ReLU(),
            nn.Conv2d(ch_out, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.GroupNorm(groups, ch_out),
            nn.ReLU(),
            nn.Conv2d(ch_out, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.GroupNorm(groups, ch_out),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.conv(x)
        return x

class conv_block4(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_block4, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=1, stride=1, padding=0, bias=True),
            nn.GroupNorm(groups,ch_out),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.conv(x)
        return x

class conv_1x1(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_1x1, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=1, stride=1, padding=0, bias=True),
            nn.GroupNorm(groups, ch_out),
            nn.ReLU()
        )

    def forward(self, x):
        x = self.conv(x)
        return x

class up_conv(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(up_conv, self).__init__()
        self.up = nn.Sequential(
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            # nn.ConvTranspose2d(ch_in, ch_out, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.GroupNorm(groups, ch_out),
            nn.ReLU()
        )

    def forward(self, x):
        x = self.up(x)
        return x

class AlexNet(nn.Module):
    def __init__(self, img_ch=10, output_ch=1):
        # 初始化网络参数
        super(AlexNet, self).__init__()

        self.Maxpool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        self.Conv1 = conv_block1(ch_in=img_ch, ch_out=int(96 * CH_FOLD2))
        self.Conv2 = conv_block2(ch_in=int(96 * CH_FOLD2), ch_out=int(192 * CH_FOLD2))
        self.Conv3 = conv_block3(ch_in=int(192 * CH_FOLD2), ch_out=int(384 * CH_FOLD2))
        self.Conv4 = conv_block4(ch_in=int(384 * CH_FOLD2), ch_out=int(384 * CH_FOLD2))

        self.Up3 = up_conv(ch_in=int(384 * CH_FOLD2), ch_out=int(192 * CH_FOLD2))
        self.Up2 = up_conv(ch_in=int(192 * CH_FOLD2), ch_out=int(96 * CH_FOLD2))
        self.Up1 = up_conv(ch_in=int(96 * CH_FOLD2), ch_out=int(1 * CH_FOLD2))

        self.Conv_1x1 = conv_1x1(int(1 * CH_FOLD2), output_ch)

        self.sigmoid = nn.Sigmoid()

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):

        count = []
        pad_value = 0
        x1 = self.Conv1(x)
        count.append(x1.shape[-1] % 2)
        x1 = self.Maxpool(x1)  # 96

        x2 = self.Conv2(x1)
        count.append(x2.shape[-1] % 2)
        x2 = self.Maxpool(x2)  # 192

        x3 = self.Conv3(x2)
        count.append(x3.shape[-1] % 2)
        x3 = self.Maxpool(x3)  # 384

        x4 = self.Conv4(x3)  # 384

        u1 = self.Up3(x4)  # 384->192
        if count[-1]:
            pad_func = nn.ConstantPad1d((0, 1, 0, 1), pad_value)
            u1 = pad_func(u1)
        u1 = u1 + x2
        u2 = self.Up2(u1)  # 192->96
        if count[-2]:
            pad_func = nn.ConstantPad1d((0, 1, 0, 1), pad_value)
            u2 = pad_func(u2)
        u3 = self.Up1(u2)  # 96->1
        if count[-3]:
            pad_func = nn.ConstantPad1d((0, 1, 0, 1), pad_value)
            u3 = pad_func(u3)

        x5 = self.Conv_1x1(u3)  # 1->1
        output = self.sigmoid(x5)
        return output
