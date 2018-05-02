"""
original code credit

credits : Prakash Vanapalli
github : https://github.com/Prakashvanapalli

"""

""" Data Preparation
I have modified the code for a more general use case
"""
import glob, os
from shutil import copyfile
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def split_train_val(input_folder, create_folder, train_folder_name, val_folder_name, test_size=0.1):
    """
    Given Input folder which contains folders of images with different classes,
    This will create a folder (create_folder) and divide the dataset into train
    and val according to the test_size and copy them to train_folder_name and val_folder_name
    which are inside the create folder.
    Mention input_image_format and test_size if the defaults doesn't work for you.
    """

    print(input_folder, create_folder, train_folder_name, val_folder_name)
    if not os.path.exists(create_folder):
        os.makedirs(create_folder)

    files_dir = glob.glob(input_folder+"/*/")
    print(files_dir)
    files = [glob.glob(i+"/*.*") for i in files_dir]
    print(len(files))

    print("files in each folder", [len(i) for i in files])
    print("Names of the files", [files[i][0].rsplit("/")[-2] for i in range(len(files))])

    for i in tqdm(range(len(files))):
    	#print(i)
    	x = files[i]
    	train, test = train_test_split(x, test_size=0.1, random_state = 42)
    	train_loc = train[0].rsplit("/")[-2]
    	print(train_loc)
    	train_loc = create_folder+"/"+train_folder_name+"/"+train_loc
    	print(train_loc)
    	if not os.path.exists(train_loc):
    		os.makedirs(train_loc)
    	for j in train:
    		copyfile(j, train_loc+"/"+j.rsplit("/")[-1])
    	test_loc = test[0].rsplit("/")[-2]
    	test_loc = create_folder+"/"+val_folder_name+"/"+test_loc
    	if not os.path.exists(test_loc):
    		os.makedirs(test_loc)
    	for m in test:
    		copyfile(m, test_loc+"/"+m.rsplit("/")[-1])

    files = glob.glob(create_folder+"/"+train_folder_name+"/*/")
    files = [glob.glob(i+"/*.*") for i  in files]
    print("total number of files in train folder: {}".format(sum([len(i) for i in files])))

    files = glob.glob(create_folder+"/"+val_folder_name+"/*/")
    files = [glob.glob(i+"/*.*") for i  in files]
    print("total number of files in val folder: {}".format(sum([len(i) for i in files])))


if __name__ == '__main__':
	source_folder = "/home/nitin/Anand/My_codes/Spikes/Classifer_on_top_of_ROI2Vec/data_500" 
	input_folder = "data"
	train_folder = "train"
	valid_folder = "valid"
	split_train_val(source_folder, input_folder, train_folder, valid_folder)
