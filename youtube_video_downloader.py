import pytube
import pandas as pd
from pytube import YouTube
import argparse
import os

def read_data(file_name):
    df = pd.read_csv(file_name)
    create_directory(df['save_location'][0]+"/full")
    create_directory(df['save_location'][0]+"/short")
    for index,url in enumerate(df['url']):
        yt = YouTube(url)
        if(df['type'][index].lower() == "full"):
            sub_folder = "/full"
        else:
            sub_folder = "/short"

        yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .first() \
        .download( filename = df['file_name'][index],output_path = df['save_location'][index] +sub_folder)

        print("URL address {} has been downloaded and saved as {} ".format(df['file_name'][index],df['save_location'][index]))

def create_directory(dir_name):
    import os
    if(os.path.isdir(dir_name)):
        print("Directory already present")
    else:
        os.makedirs(dir_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download videos from youtube')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-f', '--file',help = 'CSV Filename',required = True)
    args = parser.parse_args()
    print("File being read is {}".format(args.file))
    read_data(args.file)
