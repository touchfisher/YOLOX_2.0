"""
image_id	width	height	bbox(xywh)	source
b6ab77fd7	1024	1024	[834.0, 222.0, 56.0, 36.0]	usask_1

image_id	width	height	bbox(xmin ymin xmax ymax)	source
255b6ca9fea63f44125e5174bc932470b604c76043071522ba0ef63abb1a544b.png	481 820 604 922;655 957 732 1024;930 926 1013 1024;809 851 910 924;836 904 866 967;274 859 398 924;365 773 432 859;278 733 406 778;472 681 539 732;651 608 794 712;856 702 897 764;118 815 154 866;216 583 247 686;88 616 167 684;59 665 86 792;859 559 948 594;945 460 971 559;871 449 948 496;729 486 770 550;551 459 587 516;443 511 464 604;11 451 90 592;170 447 271 488;106 393 168 468;324 451 395 488;398 441 455 474;463 378 542 407;249 399 343 459;324 249 391 330;551 399 597 434;750 367 833 406;706 344 755 383;601 264 786 284;800 138 902 226;863 85 986 229;665 78 729 172;336 136 482 203;588 142 652 254;114 54 209 216;370 77 468 105;232 151 298 191;68 104 118 183;247 272 295 315;579 647 637 717;978 676 1002 753;342 0 386 40;680 288 712 317;502 77 533 105;121 321 156 409;46 149 88 199;216 1010 235 1024	UQ_7
"""

from xml.etree.ElementTree import Element, ElementTree, tostring,SubElement
from itertools import islice   #方便csv文件去表头工作
import argparse
import os
import csv


def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

#编辑xml文件的函数
def csvtoxml(fname, version = 21):
    with open(fname, 'r') as f:
        reader = csv.reader(f)     #读取csv文件

        a = Element('annotation')

        b = SubElement(a, 'folder')
        b.text = 'label'

        c = SubElement(a, 'filename')
        c.text=str(fname)[:-4]+'.png'    #字符串化路径，截取名称并加上格式

        c_1 = SubElement(a, 'path')
        c_1.text = 'train/%s' %c.text

        d = SubElement(a, 'source')
        d_1 =SubElement(d,'databases')
        d_1.text='Unknown'

        e=SubElement(a,'size')        #图片的大小
        e_1,e_2,e_3 = SubElement(e,'width'),SubElement(e,'height'),SubElement(e,'depth')
        e_1.text,e_2.text,e_3.text='1024','1024','3'

        f=SubElement(a,'segmented')
        f.text='0'

        #通过csv文件的内容写入xml文件
        for row in islice(reader,0,None):     #islice的作用为去掉第一行(即表头)
            list1=[]    #方便之后bbox坐标赋值

            # 比较复杂的object模块
            g = SubElement(a, 'object')
            g_1, g_2, g_3, g_4 = SubElement(g, 'name'), SubElement(g, 'pose'), \
                                SubElement(g, 'truncated'),SubElement(g, 'difficult')

            h=SubElement(g,'bndbox')   #bbox的坐标
            h_1, h_2, h_3,h_4 = SubElement(h, 'xmin'), SubElement(h, 'ymin'), SubElement(h, 'xmax'),SubElement(h, 'ymax')

            for text in row:
                list1.append(text)

            # 利用列表给bbox坐标赋值
            if version == 21:
                if list1[1]!='':       #判断元素是否为空
                    # print(list1[3].split(',')[0][1:])
                    h_1.text, h_2.text, h_3.text, h_4.text=list1[3].split(' ')[0], list1[3].split(' ')[1],\
                                                            list1[3].split(' ')[2], list1[3].split(' ')[3]

                else:
                    h_1.text, h_2.text, h_3.text, h_4.text = list1[3].split(',')[0], list1[3].split(',')[1], list1[3].split(',')[2], list1[3].split(',')[2]
            else:
                if list1[1]!='':       #判断元素是否为空
                    # print(list1[3].split(',')[0][1:])
                    h_1.text, h_2.text, h_3.text, h_4.text=list1[3].split(',')[0][1:], list1[3].split(',')[1],\
                                                        str(float(list1[3].split(',')[0][1:])+float(list1[3].split(',')[2])),\
                                                        str(float(list1[3].split(',')[1])+float(list1[3].split(',')[3][:-1]))

                else:
                    h_1.text, h_2.text, h_3.text, h_4.text = list1[3].split(',')[0], list1[3].split(',')[1], list1[3].split(',')[2], list1[3].split(',')[2]

            judge = str(row[-1])


            g_1.text, g_2.text, g_3.text, g_4.text = judge, 'Unspecified', '0', '0'


        #打印出
        print(str(c.text)+'   ----> True')


    return ElementTree(a)



#方便引入文件、路径
if __name__ == '__main__':
    

    # step 0 定义
    
    single_csv_path = 'sc'
    create_dir_not_exist(single_csv_path )
    way_2 = 'xml'
    create_dir_not_exist(way_2)

    w_size = str(1024)# 图片尺寸, 其实问题不大, 给21版本的查缺补漏用的
    h_size = str(1024)

    version = 20 # 数据集版本

    if version == 21:
        fname = 'competition_test.csv'
    else:
        fname = 'train.csv'
	
	# step I 将csv文档拆分为3373个小csv文档
    flag_detatch = 1
    if flag_detatch:
        # step 1.1 读取文档, 生成name list 和 class list
            with open(fname, 'r') as f:
                reader = csv.reader(f) 
                list_name=[]
                list_class=[]
                for row in islice(reader,1,None): 
                    if row[0] not in list_name:
                        list_name.append(row[0])
                    if row[-1] not in list_class:
                        list_class.append(row[-1])
                print(len(list_name), list_class)
            if version == 21:
            # step 1.2 根据name list 生成对应csv文件
                for name in list_name:
                    # print(name)
                    with open(fname, 'r') as f:             # 打开csv文档
                        reader = csv.reader(f)              # 加载文档内容
                        for row in islice(reader,1,None):   # 
                            if row[0]==name:
                                new_name = './sc/'+ name.split('.')[0] + '.csv'
                                print(new_name)
                                bbox_list = list(row[1].split(';'))
                                for bbox in bbox_list:
                                    if bbox != 'no_box':# 剔除没有目标的图片
                                        
                                        new_row = []
                                        new_row.append(name.split('.')[0])#新的内容拼接
                                        new_row.append(w_size)
                                        new_row.append(h_size)
                                        new_row.append(bbox)
                                        new_row.append(row[-1])

                                        f = open(new_name,'a',newline = '')# 打开新建的csv文档进行写入
                                        writer = csv.writer(f)
                                        writer.writerow(new_row)
                                        f.close()
            else:
            # step 1.2 根据name list 生成对应csv文件
                for name in list_name:
                    # print(name)
                    with open(fname, 'r') as f:
                        reader = csv.reader(f)
                        for row in islice(reader,1,None): 
                            if row[0]==name:
                                new_name = './sc/'+ name + '.csv'
                                print(new_name)
                                f = open(new_name,'a',newline = '')
                                writer = csv.writer(f)
                                writer.writerow(row)
                                f.close()
    flag_transform = 1
    if flag_transform:
        # step II 分别对每个csv文档进行数据提取, 并格式化
        #遍历该文件夹
        for filename in os.listdir(r"%s" % single_csv_path):
    
            name = filename[:-4]
    
            tree=csvtoxml(r'%s\%s.csv'%(single_csv_path,name), version)
            tree.write('%s/%s.xml'% (way_2,name), encoding='UTF-8')

