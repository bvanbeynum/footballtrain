import subprocess
import os
import re
import time

startTime = time.time()

videoDir = "./files/video/"
frameDir = "./files/frame/"

for file in os.listdir(videoDir):
	fileRE = re.search(r"([^.]+).mp4", file, flags=re.IGNORECASE)
	
	if (fileRE):
		fileName = fileRE.group(1)
		
		print(str(round(time.time() - startTime)) + ": Processing file " + fileName)
		subprocess.run("ffmpeg -i " + videoDir + file + " -vf \"scale=320:240, fps=4\" " + frameDir + fileName + "_%d_category.jpg", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		
		os.remove(videoDir + file)

print(str(round(time.time() - startTime)) + ": Done!")
