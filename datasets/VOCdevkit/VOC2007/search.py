import os

a = os.listdir(r'C:\Users\16325\Desktop\YOLOX-main\datasets\VOCdevkit\VOC2007\Annotations')
b = os.listdir(r'C:\Users\16325\Desktop\YOLOX-main\datasets\VOCdevkit\VOC2007\JPEGImages')
print(len(a),len(b))

c = []
for i in range(len(a)):
    a[i]=a[i][:-4]
for i in range(len(b)):
    b[i]=b[i][:-4]

a = set(a)
b = set(b)

print(a^b==b-a)
c=a^b

for i in c:
    path=r'C:\Users\16325\Desktop\YOLOX-main\datasets\VOCdevkit\VOC2007\JPEGImages'+'\\'+i+'.jpg'
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)  
    else:
        print('no such file:%s'%path)  # 则返回文件不存在

