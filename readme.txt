Configuration required:
puthon-3.8
numpy-1.24.4
pandas-1.5.3
pytorch-1.10.1
cuda-11.3.1

The contents of each file:
The "data" folder contains both the original data and the data we used
The files 'data_set.py' and 'dataset.py' are used for data preprocessing, primarily converting RNA data into matrices for model input.
The 'FCN_U.py' file is the main code of the model.
The 'train_U.py' file is the main training process.
The 'test1.py' file is used for data preprocessing of the test set and generation of the pairwise probability matrix.
The 'PostProcessing.py' file is designed for performing relevant post-processing operations on the generated pairing probability matrix.
"trained_model_U_A7.pth" is the weight trained by the model
Usage:
Run the main function in the PostProcessing file, directly input an RNA sequence, and the result will be generated. The pairing probability matrix 2.txt file generated during the running process is the pairing probability matrix for this sequence.


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
