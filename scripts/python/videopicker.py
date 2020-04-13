import os
import re
import random
import time
import requests

startTime = time.time()

folders = ["./files/e/2019-10-05", "./files/e/2019-09-28", "./files/e/2019-09-21", "./files/e/2019-09-14"]

# "./files/d/2019-10-12", "./files/d/2019-10-19", "./files/d/2019-10-27"

for folder in folders:
	files = []

	for file in os.listdir(folder):
		if (re.search(r"([^.]+).mp4", file, flags=re.IGNORECASE)):
			files.append(folder + "/" + file)

	randomFiles = random.sample(files, int(len(files) * .2))

	print(str(round(time.time() - startTime)) + " uploading " + str(len(randomFiles)) + " of " + str(len(files)) + " from " + folder)

	for index, randomFile in enumerate(randomFiles):
		print(str(round(time.time() - startTime)) + " uploading " + str(index + 1) + ": " + randomFile)
		fileReader = open(randomFile, "rb")
		uploadFile = { randomFile: fileReader }
		response = requests.post("http://huntingtonbeach.beynum.com/uploadvideo", files=uploadFile)
		fileReader.close()

	print(str(round(time.time() - startTime)) + " completed " + folder)
