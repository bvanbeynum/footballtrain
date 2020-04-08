import subprocess
import os
from datetime import datetime
import glob
import re
import requests
import time

startTime = time.time()
videoPath = os.curdir + "/videos"
framePath = os.curdir + "/frames"

#[\d]{4}-[\d]{2}-[\d]{2}[-\d]*.jpg

for file in glob.glob(videoPath + "/*.mp4"):
    fileRE = re.search(r".\/videos\\([^.]+).mp4", file, flags=re.IGNORECASE)
    fileName = fileRE.group(1)

    print(str(round(time.time() - startTime)) + ": Processing file " + fileName)
    subprocess.run("./ffmpeg.exe -i " + file + " -vf \"scale=320:240, fps=2\" frames/" + fileName + "_%d_category.jpg", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(str(round(time.time() - startTime)) + ": Uploading from file " + fileName)
    
    for frameFile in glob.glob(framePath + "/*.jpg"):
        if re.search(fileName, frameFile):
            fileReader = open(frameFile, "rb")
            uploadFile = { frameFile: fileReader }
            response = requests.post("http://dev.beynum.com:8080/upload", files=uploadFile)
            fileReader.close()
            os.remove(frameFile)
    
    os.remove(file)

print(str(round(time.time() - startTime)) + ": Done!")