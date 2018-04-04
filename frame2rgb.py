# python dependencies
import os
import colorgram
import json
import glob

source_folder_images = '/home/nitin/Anand/Datasets/friends/frames'
destination_folder_rgb = '/home/nitin/Anand/Datasets/friends/frames_rgb/'

COLOR = "Color"
PIXEL_FRACTION = "Pixel Fraction"
RED = "Red"
GREEN = "Green"
BLUE = "Blue"
DOMINANT_COLORS = "dominantColors"

for folder in glob.glob(source_folder_images+'/*'):
	folder_name = folder.split("/")[-1]
	for image in glob.glob(folder + '/*'):
		colors = colorgram.extract(image, 8) # 8 means 8 dominant colors
		image_name = image.split("/")[-1].split(".")[0]
		Colors = {}
		Colors[COLOR] = {}
		col = []
		for i in range(len(colors)):
		    color_class = colors[i]
		    rgb_value = color_class.rgb
		    percent = color_class.proportion
		    RGB_Values = rgb_value[0:3]                  
		    Colors[COLOR][RED] = RGB_Values[0]
		    Colors[COLOR][GREEN] = RGB_Values[1]
		    Colors[COLOR][BLUE] = RGB_Values[2]
		    Colors[PIXEL_FRACTION] = percent
		    col.append(Colors)
		    Colors = {}
		    Colors[COLOR] = {}
		dominantColors = {}
		dominantColors[DOMINANT_COLORS] = col 
		print(dominantColors)
		filename = destination_folder_rgb + folder_name +"/"+ image_name + ".json"
		if filename:
		    with open(filename, 'w') as f:
		        json.dump(dominantColors, f,sort_keys=True, indent=4)
