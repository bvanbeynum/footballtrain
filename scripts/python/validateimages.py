import tensorflow as tf
from tensorflow.keras import models

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os
import time
import re
import random
import numpy as np

startTime = time.time()
categories = ["start", "qb", "player", "air", "end", "other"]
frameDir = "../frames"
modelFolder = "trainlog\model_1599192785"
files = []

model = models.load_model(f"{modelFolder}\model")

print(str(round(time.time() - startTime)) + ": Load Files")

for file in os.listdir(frameDir):
	fileRE = re.search(r"^([^_]+)_([\d]+)_([^\.]+).jpg", file, flags = re.IGNORECASE)

	if fileRE:
		fileName = fileRE.group(1)
		frame = int(fileRE.group(2))
		category = fileRE.group(3)
		
		existing = list(filter(lambda file: file["name"] == fileName, files))
		if len(existing) > 0:
			existing[0]["frames"].append({ "path": os.path.join(frameDir, file), "category": category, "frame": frame })
			existing[0]["frames"] = sorted(existing[0]["frames"], key = lambda frames: frames["frame"])
		else:
			files.append({ "name": fileName, "frames": [{ "path": os.path.join(frameDir, file), "category": category, "frame": frame }]})

print(str(round(time.time() - startTime)) + ": Files loaded - " + str(len(files)))

random.shuffle(files)

imageWidth = 256
imageHeight = 192
textWidth = 50
textHeight = 17
font = ImageFont.truetype("impact.ttf", 16)

for file in files:
	print(str(round(time.time() - startTime)) + ": Processing - " + file["name"])

	base = Image.new("RGB", (imageWidth * len(files[0]["frames"]), imageHeight), (255,255,255))
	draw = ImageDraw.Draw(base)

	for index, frame in enumerate(files[0]["frames"]):
		image = Image.open(frame["path"]).resize((imageWidth, imageHeight))
		imageArray = np.asarray(image).reshape(-1, imageHeight, imageWidth, 3)
		frame["prediction"] = model.predict([imageArray])

		base.paste(image, (index * imageWidth, 0))

		lineStart = (((index + 1) * imageWidth) - 3, 0)
		lineEnd = (((index + 1) * imageWidth) - 3, imageHeight)
		draw.line([lineStart, lineEnd], fill="black", width=3)

		textPosition = [((index + 1) * imageWidth) - textWidth, (categories.index(category) * 31) + 7]

		for category in categories:
			if category == frame["category"] and categories.index(category) == frame["prediction"][0].argmax():
				textColor = "blue"
			elif category == frame["category"]:
				textColor = "yellow"
			elif categories.index(category) == frame["prediction"][0].argmax():
				textColor = "red"
			else:
				textColor = "white"
			
			textPosition = [(index * imageWidth) + 5, (categories.index(category) * 31) + 7]
			text = category.upper() + " - " + str(round(frame["prediction"][0][categories.index(category)] * 100, 2)) + "%"

			# Draw outline
			draw.text((textPosition[0] - 1, textPosition[1] - 1), text, font=font, fill="black")
			draw.text((textPosition[0] + 1, textPosition[1] - 1), text, font=font, fill="black")
			draw.text((textPosition[0] - 1, textPosition[1] + 1), text, font=font, fill="black")
			draw.text((textPosition[0] + 1, textPosition[1] + 1), text, font=font, fill="black")

			# Draw text
			draw.text(textPosition, text, font=font, fill=textColor)

	base.save(modelFolder + "\\files\\" + file["name"] + ".jpg")
	# base.show()

print(str(round(time.time() - startTime)) + ": completed - " + str(len(files)))