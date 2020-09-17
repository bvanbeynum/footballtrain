import os
import re
import random
import time
import requests

startTime = time.time()
loadFolder = "../videos/load"
filesLoaded = 0

for file in os.listdir(loadFolder):
	if (re.search(r"([^.]+).mp4", file, flags=re.IGNORECASE)):
		print(str(round(time.time() - startTime)) + " uploading: " + file + " - #" + str(filesLoaded + 1))
		fileReader = open(loadFolder + "/" + file, "rb")
		uploadFile = { "file": fileReader }
		response = requests.post("http://huntingtonbeach.beynum.com:9006/uploadvideo", files=uploadFile)
		fileReader.close()
		filesLoaded += 1

print(str(round(time.time() - startTime)) + " completed " + str(filesLoaded))
