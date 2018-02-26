# import urllib
from bs4 import BeautifulSoup
import urllib.request
# import pandas as pd
# from urllib.error import URLError
# from multiprocessing import Pool
# from functools import partial
# import sys
# import time
import requests
import os
import urllib3
import argparse
import pandas as pd

def download(searchtext,num_requested):

    #string initializations
    main_website = "https://archive.org"
    compress_download = "/compress/"
    #middle_string = "/formats=H.264&file=/"
    middle_string = "/formats=OGG VIDEO&file=/"
    video_download = "/download/"

    #urllib3 initializations
    urllib3.disable_warnings()
    http = urllib3.PoolManager()

    #create url to scrape
    searchtext_list = searchtext.split(" ")
    if(len(searchtext_list) == 1):
        url = "https://archive.org/search.php?query={}".format(searchtext_list[0])
    elif(len(searchtext_list) == 2):
        url = "https://archive.org/search.php?query={} {}".format(searchtext_list[0],searchtext_list[1])

    #initialize soup and scrape
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    video_list = soup.findAll("a", {"data-event-click-tracking": "GenericNonCollection|ItemTile"})

    downloaded_video_count = 0
    for video in video_list:
        video_id = video['href'].split('/')[-1]
        video_name = video_id + ".zip"
        video_url = main_website + compress_download + video_id + middle_string + video_id + ".zip"
        print(video_name,video_url)
        r = http.request('GET', video_url, preload_content=False)
        if(r.status == 200):
            print(r.status)
            with open(video_name, 'wb') as out:
                data = r.data
                out.write(data)
                out.close()
                downloaded_video_count = downloaded_video_count +1
        else:
            video_page_url = main_website + video['href']
            soup_video_page = BeautifulSoup(requests.get(video_page_url).text, 'html5lib')
            video_list = soup.findAll("a", {"class": "format-summary"})
            for video in video_list:
                if (video['href'].split('.')[-1] == 'mp4'):
                    video_url = main_website + video['href']
                    print(video_name,video_url)
                    r = http.request('GET', video_url, preload_content=False)
                    if(r.status == 200):
                        with open(video_name, 'wb') as out:
                            data = r.data
                            out.write(data)
                            out.close()
                            downloaded_video_count = downloaded_video_count +1
        print("Here",downloaded_video_count)
        if(downloaded_video_count >= num_requested):
            break

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download videos')
	required = parser.add_argument_group('required arguments')
	required.add_argument('-f', '--file',help = 'CSV Filename',required = True)
	args = parser.parse_args()
	print("File being read is {}".format(args.file))
	df = pd.read_csv(args.file)
	for index,searchtext in enumerate(df['searchtext']):
		download(searchtext,df['num_requested'][index])
