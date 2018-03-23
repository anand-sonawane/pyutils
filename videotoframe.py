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
		for i in range(0,5000):
			success,frame = vidcap.read()
			if(success):
				frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				fm = variance_of_laplacian(gray)
				fm_array.append(fm)
	fm_numpy = np.array(fm_array)
	threshold = np.percentile(fm_numpy, 0)
	threshold1 = np.percentile(fm_numpy, 20)
	threshold2 = np.percentile(fm_numpy, 40)
	threshold3= np.percentile(fm_numpy, 50)
	threshold4 = np.percentile(fm_numpy, 90)
	print(threshold,threshold1,threshold2,threshold3,threshold4)
	vidcap.release()
	return threshold3

input_dir_name = "/home/nitin/Anand/Datasets/Sportcast/Videos/short"
output_dir_name = "/home/nitin/Anand/Datasets/Sportcast/Videos_to_frame/short1"

onlyfiles = [f for f in listdir(input_dir_name) if isfile(join(input_dir_name, f))]
print(onlyfiles)

for file_name in onlyfiles:
	file_name_input = input_dir_name + "/" + file_name
	temp_file_name = (file_name.split('/')[-1].split('.')[0]).replace(" ","_")
	file_name_output = output_dir_name + "/" + temp_file_name
	threshold = get_threshold(file_name_input)
	#threshold = 150.0
	print(file_name_input,threshold)
	if not os.path.exists(file_name_output):
		os.makedirs(file_name_output)
	vidcap = cv2.VideoCapture(file_name_input)
	success,frame = vidcap.read()
	print(success)
	count = 0
	count_frame = 0
	while success:
		count_frame += 1
		if(count_frame%30==0):
			success,frame = vidcap.read()
			#print(success,frame)
			if(success):
				frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				fm = variance_of_laplacian(gray)
				#print(fm,threshold)
				if fm > threshold:
					value = cv2.imwrite(os.path.join(file_name_output, "frame%d.jpg" % count_frame), frame)
					count += 1
	vidcap.release()
	print("Total frames for this file :",count)

