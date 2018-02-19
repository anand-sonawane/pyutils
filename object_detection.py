def IOU(boxA, boxB):
	import numpy as np
	import cv2
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
 
	# compute the area of intersection rectangle
	interArea = (xB - xA + 1) * (yB - yA + 1)
 
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
 
	# return the intersection over union value
	return iou

def video_to_frame(videofile_path):
	import cv2
	import os

	dirname = videofile_path.split('/')[-1].split(".")[0]
	if(!os.path.isdir(dirname)):
		mkdir(dirname)
	vidcap = cv2.VideoCapture(videofile_path)
	success,image = vidcap.read()
	print(success,image)
	count = 0
	success = True
	while success:
	  success,image = vidcap.read()
	  print('Read a new frame: ', success)
	  cv2.imwrite(os.path.join(dirname, "frame%d.jpg" % count), image)
	  count += 1
