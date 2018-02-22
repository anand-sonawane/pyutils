from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib3
import sys
import pandas as pd
import time
import argparse

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"
urllib3.disable_warnings()

def download(searchtext,num_requested):
	http = urllib3.PoolManager()
	searchtext = searchtext
	num_requested = num_requested
	number_of_scrolls = int(num_requested / 400 + 1)
	# number_of_scrolls * 400 images will be opened in the browser

	if not os.path.exists(download_path + searchtext.replace(" ", "_")):
		os.makedirs(download_path + searchtext.replace(" ", "_"))

	url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
	driver = webdriver.Chrome()
	driver.get(url)

	extensions = {"jpg", "jpeg", "png", "gif"}
	img_count = 0
	downloaded_img_count = 0

	for _ in range(number_of_scrolls):
		for __ in range(10):
			# multiple scrolls needed to show all 400 images
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		# to load next 400 images
		time.sleep(0.5)
		try:
			driver.find_element_by_xpath("//input[@value='Show more results']").click()
		except Exception as e:
			print("Less images found:", e)
			break

	# imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
	imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
	print("Total images:", len(imges), "\n")
	for img in imges:
		img_count += 1
		img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
		img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
		print("Downloading image", img_count, ": ", img_url)
		for extension in extensions:
			if extension in img_url:
				try:
					r = http.request('GET', img_url, preload_content=False)
					with open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, 'wb') as out:
						data = r.data
						out.write(data)
						out.close()
						downloaded_img_count += 1
				except Exception as e:
					print("Download failed:", e)
				finally:
					print()
		if downloaded_img_count >= num_requested:
			break

	print("Total downloaded: ", downloaded_img_count, "/", img_count)
	driver.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Download images from google image search')
	required = parser.add_argument_group('required arguments')
	required.add_argument('-f', '--file',help = 'CSV Filename',required = True)
	args = parser.parse_args()
	print("File being read is {}".format(args.file))
	df = pd.read_csv(args.file)
	for index,searchtext in enumerate(df['searchtext']):
		download(searchtext,df['num_of_images'][index])