import os
import json
import colorgram
import time
from colour import Color
import webcolors
from webcolors import rgb_to_name
from collections import defaultdict
import glob

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour[:3])
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def dumps_json_in_files(json_file, json_data):
    file_status = False
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)
        file_status = True
    return file_status

source_folder_rgb = ''
destination_folder_colorname = ''

for folder in glob.glob(source_folder_rgb+'/*'):
    folder_name = folder.split("/")[-1]
    for image in glob.glob(folder + '/*'):
        colors = colorgram.extract(image, 8) # 8 means 8 dominant colors
        #colors = colorgram.extract(image, 6) # 4 means 8 dominant colors
        image_name = image.split("/")[-1].split(".")[0]
        colors_name = defaultdict(list)
        for i in range(len(colors)):
            color_class = colors[i]
            rgb_value = color_class.rgb
            percent = color_class.proportion
            RGB_Values = rgb_value[0:3]                  
            actual_name, closest_name = get_colour_name(RGB_Values)
            colors_name[closest_name].append(percent*100)
        final_dict = {}
        for key, values in colors_name.items():
            final_dict[key] = sum(values)
        palettes = {}
        palettes['Color_Palette'] = final_dict
        print(palettes)
        filename = destination_folder_colorname + folder_name +"/"+ image_name + ".json"
        if filename:
            with open(filename, 'w') as f:
                json.dump(palettes, f,sort_keys=True, indent=4)
