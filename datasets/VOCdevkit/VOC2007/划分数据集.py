import os
import random

trainval_percent = 0.9
train_percent = 0.9
xmlfilepath = r'C:\Users\16325\Desktop\YOLOX-main\datasets\VOCdevkit\VOC2007\Annotations'
home = r"C:\Users\16325\Desktop\YOLOX-main\datasets\VOCdevkit\VOC2007\ImageSets\Main\\"
#txtsavepath = '/home/ubuntu/tf-faster-rcnn-master/data/VOCdevkit2007/VOC2007/ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

ftrainval = open(home+'trainval.txt', 'w')
ftest = open(home+'test.txt', 'w')
ftrain = open(home+'train.txt', 'w')
fval = open(home+'val.txt', 'w')

for i  in list:
    name=total_xml[i][:-4]+'\n'
    #trainval为训练用到的全部数据，含训练集和验证集
    if i in trainval:
        ftrainval.write(name)
        #测试集数据
        if i in train:
            ftrain.write(name)
        #验证集数据
        else:
            fval.write(name)
    #不在trainval中的数据，说明为测试集
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()