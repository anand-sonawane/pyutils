import cv2
import os
from os import listdir
from os.path import isfile, join
from os import walk
from imutils import paths
import argparse
import cv2
import numpy as np

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def get_threshold(file_name):
	vidcap = cv2.VideoCapture(file_name)
	success,frame = vidcap.read()
	fm_array = []
	print(success)
	if(success):
		count = 0
		for i in range(0,100):
			while success:
				 success,frame = vidcap.read()
				 frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
				 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				 fm = variance_of_laplacian(gray)
				 fm_array.append(fm)
	fm_numpy = np.array(fm_array)
	threshold = np.percentile(fm_numpy, 20)
	return threshold


dirname = "test"
input_dir_name = "/home/nitin/Anand/Datasets/Sportcast/Videos/full"
output_dir_name = "/home/nitin/Anand/Datasets/Sportcast/Videos_to_frame/full"

onlyfiles = [f for f in listdir(input_dir_name) if isfile(join(input_dir_name, f))]
print(onlyfiles)

for file_name in onlyfiles:
	threshold = get_threshold(file_name)
	vidcap = cv2.VideoCapture(file_name)
	success,frame = vidcap.read()
	print(success)
	if(success):
		count = 0
		while success:
			 success,frame = vidcap.read()
			 frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
			 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			 fm = variance_of_laplacian(gray)
			 if fm > threshold:
				cv2.imwrite(os.path.join(output_dir_name,file_name.split('/')[-1].split('.')[0], "frame%d.jpg" % count), frame)
			 	count += 1
	print("Total frames for this file :",count)

