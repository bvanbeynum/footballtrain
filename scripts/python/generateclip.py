import tensorflow as tf
from tensorflow.keras import models

import PIL
from PIL import Image

import numpy as np
import os
import time
import re
import subprocess
import math

startTime = time.time()
categories = ["start", "qb", "player", "air", "ground", "missing"]
videoDir = "../videos"
workingDir = videoDir + "/working"
modelFolder = "trainlog/model_1599192785"

imageWidth = 640
imageHeight = 480

model = models.load_model(modelFolder + "/model")

for file in os.listdir(videoDir):
	fileRE = re.search(r"([^.]+).mp4", file, flags=re.IGNORECASE)
	
	if fileRE:
		fileName = fileRE.group(1)
		print(str(round(time.time() - startTime)) + ": Getting frames for " + fileName)

		subprocess.run("ffmpeg.exe -i " + videoDir + "/" + file + " -vf \"scale=" + str(imageWidth) + ":" + str(imageHeight) + ", fps=2\" " + workingDir + "/" + fileName + "_%d.jpg", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		print(str(round(time.time() - startTime)) + ": Running predictions")
		
		frames = []
		for frame in os.listdir(workingDir):
			fileRE = re.search(r"^[^_]+_([\d]+).jpg", frame, flags=re.IGNORECASE)
			
			if fileRE:
				image = Image.open(workingDir + "/" + frame)
				imageArray = np.asarray(image).reshape(-1, imageHeight, imageWidth, 3)
				prediction = model.predict([imageArray])

				frames.append({ "id": int(fileRE.group(1)), "prediction": categories[prediction[0].argmax()] })
			
			os.remove(workingDir + "/" + frame)

		frames = sorted(frames, key = lambda frameA: frameA["id"])
		
		continousCounter = 0
		start = 0
		end = 0
		for index, frame in enumerate(frames):
			if index == 0:
				continousCounter = 1
			elif start == 0 and frame["prediction"] in ["air", "player"] and frames[index - 1]["prediction"] in ["air", "player"]:
				continousCounter += 1
			elif start > 0 and frame["prediction"] == "end" and frames[index - 1]["prediction"] == "end":
				continousCounter += 1
			else:
				continousCounter = 1
			
			if start == 0 and continousCounter >= 3 and frame["prediction"] in ["air", "player"]:
				start = index
			
			if start > 0 and continousCounter >= 3 and frame["prediction"] == "end":
				end = index
				break
		
		if start > 0 or end > 0:
			print(str(round(time.time() - startTime)) + ": Generating clip starting on frame " + str(start) + " to " + str(end))
		
			if start > 0:
				clipStart = "-ss 00:"

				if (start - 3) / 2 > 60:
					clipStart += ("00" + str(math.floor(((start - 3) / 2) / 60)))[-2:] + ":" + ("00" + str(math.floor((start - 3) / 2) % 60))[-2:]
				else:
					clipStart += "00:" + ("00" + str(math.floor((start - 3) / 2)))[-2:]
			else:
				clipStart = ""

			if end > 0 and end + 3 <= len(frames):
				clipEnd = (end + 3) / 2
			else:
				clipEnd = ""

			subprocess.run("ffmpeg.exe " + clipStart + " -i " + videoDir + "/" + file + " -s 180x135 -f gif " + videoDir + "/clips/" + fileName + "_clip.gif", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else:
			print(str(round(time.time() - startTime)) + ": Could not find clip")
