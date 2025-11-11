需要配置:
puthon-3.8
numpy-1.24.4
pandas-1.5.3
pytorch-1.10.1
cuda-11.3.1

各个文件的内容：
data文件夹中包含了原始数据以及本论文所使用的数据
data_set.py和dataset.py文件用于进行数据的预处理，主要将RNA数据转化成矩阵用于模型的输入。
FCN_U.py文件是模型的主要代码。
train_U.py文件是主要的训练过程。
test1.py文件用于测试集的数据预处理以及配对概率矩阵的生成。
PostProcessing.py文件是针对于生成的配对概率矩阵进行相关的后处理操作。
trained_model_U_A7.pth是模型训练出的权重
使用方法：
在PostProcessing文件中运行main函数，直接输入一条RNA序列，即可运行出结果，在运行过程中会生成的配对概率矩阵2.txt文件是这条序列的配对概率矩阵。