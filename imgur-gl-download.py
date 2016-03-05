#! /usr/bin/env python

import requests
import sys
import os

client_id = '!!!!<your_cliend_id_here>!!!!';
chunk_size = 1024;
silent = 0;
download_folder = "";
curr=0;
total=0;

def main():
	gallery_id = "";

	#Input args
	
	if(len(sys.argv) > 1):
		if(sys.argv[1].find('/')):
			gallery_id = sys.argv[1].split('/')[-1];
		else:
			gallery_id = sys.argv[1];
	else:
		print("No gallery ID provided; downloading a sample dank memes gallery.");
		gallery_id = "OIoXq";

	global download_folder; #Didn't know about the usage of global. Good to know. :D

	if(len(sys.argv) > 2):
		download_folder = sys.argv[2];
	else:
		download_folder = gallery_id + "/";

	#Actual stuff
	header = {"Authorization": "Client-ID " + client_id};
	r = requests.get("https://api.imgur.com/3/gallery/album/%s" % gallery_id, headers=header);
	r = r.json();
		
	if(r['status'] != 200):
		print("Something went wrong. Error code: %s" % r['status']);
		exit();
	r = r['data']['images'];
	
	global count;
	count = len(r);
	global curr;
	for img in r:
		#print(img['link']);
		curr = curr + 1;
		download_img(img['link']);

def download_img(link):
	filename = link.split('/')[-1];
	#print download_folder;
	filename = download_folder + filename;

	#create directory if it doesn't exist
	if not os.path.exists(download_folder):
		os.makedirs(download_folder);

	print(str.format("Saving to {0} | {1} of {2}", filename, str(curr), str(count)));

	r = requests.get(link, stream=True);
	with open(filename, 'wb') as fw:
		for chunk in r.iter_content(chunk_size):
			fw.write(chunk);

if __name__ == "__main__":
	main();
