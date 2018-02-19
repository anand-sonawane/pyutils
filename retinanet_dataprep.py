from xml.dom.minidom import parse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile,join
import math

#path of annotations folder
dir_parent = '/home/nitin/Anand/Datasets/pascal voc/VOCdevkit/VOC2012/'
dir_anno = dir_parent + "Annotations"
files= [f for f in listdir(dir_anno) if isfile(join(dir_anno, f))]
files_subset = files[0:200]

print("Total Files {} and Subset Contains {}".format(len(files),len(files_subset)))

#17125*0.8 = 13700
files_train = files[0:13700]
files_valid = files[13700:]
print("Total Files {} ,Train contains {} and validation contains {} ".format(len(files),len(files_train),len(files_valid)))

pd.DataFrame(files_train,columns = ['filename']).to_csv("Train_list.csv")
pd.DataFrame(files_valid,columns = ['filename']).to_csv("Valid_list.csv")

train_file_path = 'Train_list.csv'
valid_file_path = 'Valid_list.csv'

files_train = pd.read_csv(train_file_path).filename.tolist()
files_valid = pd.read_csv(valid_file_path).filename.tolist()

print("Train contains {} Images and validation contains {} Images".format(len(files_train),len(files_valid)))

#path_paperspace = "/home/paperspace/retinanet/VOCdevkit/VOC2012/Annotations"
dir_images = dir_parent + "JPEGImages"

train_list = []
for file in files_train:
    tree = ET.parse('{}/{}'.format(dir_anno,file))
    root = tree.getroot()
    filename = dir_images + "/" +root.find('filename').text
    for each_object in root.findall('object'):
        obj_name = each_object.find('name').text
        x1 = math.floor(float(each_object.find('bndbox').find('xmin').text))
        y1 = math.floor(float(each_object.find('bndbox').find('ymin').text))
        x2 = math.floor(float(each_object.find('bndbox').find('xmax').text))
        y2 = math.floor(float(each_object.find('bndbox').find('ymax').text))
        train_list.append([filename,x1,y1,x2,y2,obj_name])


valid_list = []
for file in files_valid:
    tree = ET.parse('{}/{}'.format(dir_anno,file))
    root = tree.getroot()
    filename = dir_images + "/" + root.find('filename').text
    for each_object in root.findall('object'):
        obj_name = each_object.find('name').text
        x1 = math.floor(float(each_object.find('bndbox').find('xmin').text))
        y1 = math.floor(float(each_object.find('bndbox').find('ymin').text))
        x2 = math.floor(float(each_object.find('bndbox').find('xmax').text))
        y2 = math.floor(float(each_object.find('bndbox').find('ymax').text))
        valid_list.append([filename,x1,y1,x2,y2,obj_name])

print("Train contains {} Objects and validation contains {} Objects".format(len(train_list),len(valid_list)))

train_data = pd.DataFrame(train_list,columns = ['image_name','xmin','ymin','xmax','ymax','label'])
valid_data = pd.DataFrame(valid_list,columns = ['image_name','xmin','ymin','xmax','ymax','label'])

train_data.to_csv("pascalvoc_retinanet_train.csv")
valid_data.to_csv("pascalvoc_retinanet_valid.csv")

pd.DataFrame(train_data.label.unique().tolist()).to_csv("pascalvoc_retinanet_classes.csv")