import os
import glob
from sklearn.model_selection import train_test_split

dir_path = os.getcwd()
source_folder = '/home/nitin/Anand/Datasets/Sportcast/All_data_6April/Entities/All_annotations'

filename_list = []
for file in glob.glob(source_folder+'/*'):
	fi = file.split('/')[-1].rsplit('.',1)[0]
	print(fi)
	filename_list.append(fi)
print(filename_list)

train, test = train_test_split(filename_list, test_size=0.1, random_state = 42)

count_train = 0
f = open("train_1.txt", 'w')
for index,filename in enumerate(train):
	line = filename+'\n'
	print(line)
	count_train += 1
	f.write(line)
f.close()

count_val = 0
f = open("val_1.txt", 'w')
for index,filename in enumerate(test):
	line = filename+'\n'
	print(line)
	count_val += 1
	f.write(line)
f.close()

print(count_train + count_val)