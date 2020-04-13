import subprocess
import os
import re
import time

startTime = time.time()

videoDir = "./files/video/"
frameDir = "./files/frame/"

files = []

for file in os.listdir(videoDir):
	fileRE = re.search(r"([^.]+).mp4", file, flags=re.IGNORECASE)
	
	if (fileRE):
		files.append({"file": file, "fileName": fileRE.group(1)})

print(str(round(time.time() - startTime)) + ": " + str(len(files)) + " files")

for index, file in enumerate(files):
	print(str(round(time.time() - startTime)) + ": Processing file " + str(index) + ", " + file["fileName"])
	subprocess.run("ffmpeg -i " + videoDir + file["file"] + " -vf \"scale=640:480, fps=4\" " + frameDir + file["fileName"] + "_%d_category.jpg", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	
	os.remove(videoDir + file["file"])

print(str(round(time.time() - startTime)) + ": Done!")
