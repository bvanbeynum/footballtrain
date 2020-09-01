import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
# from tensorflow.keras.callbacks import TensorBoard
import sklearn
from sklearn.model_selection import train_test_split
import numpy as np
import os
import time
import re
import random

startTime = time.time()
categories = ["start", "qb", "player", "air", "end", "other"]
files = []
images = []
labels = []
results = []
maxFiles = 30

frameDir = "../frames"

print(str(round(time.time() - startTime)) + ": Starting")

for file in os.listdir(frameDir):
	fileRE = re.search(r"^([^_]+)_([\d]+)_([^\.]+).jpg", file, flags = re.IGNORECASE)

	if fileRE: # and fileRE.group(3) != "other":
		fileName = fileRE.group(1)
		frame = fileRE.group(2)
		category = fileRE.group(3)
		
		existing = list(filter(lambda file: file["name"] == fileName, files))
		if len(existing) > 0:
			existing[0]["frames"].append({ "path": os.path.join(frameDir, file), "category": category })
		else:
			files.append({ "name": fileName, "frames": [{ "path": os.path.join(frameDir, file), "category": category }]})

randomFiles = random.sample(files, maxFiles)
files = []

for file in randomFiles:
	for frame in file["frames"]:
		image = load_img(frame["path"], target_size=(192,256))
		# image = load_img(frame["path"])

		imageArray = img_to_array(image)
		imageArray = imageArray / 255.0
		imageArray = np.array(imageArray)
		
		images.append(imageArray)
		labels.append(categories.index(frame["category"]))

print(str(round(time.time() - startTime)) + ": files - " + str(len(randomFiles)) + " / Images loaded - " + str(len(images)))

imagesTrain, imagesTest, labelsTrain, labelsTest = train_test_split(images, labels, test_size=0.3, random_state=0)

imagesTrain = np.array(imagesTrain)
imagesTest = np.array(imagesTest)
labelsTrain = np.array(labelsTrain)
labelsTest = np.array(labelsTest)

denseLayers = [0,1,2]
layerSizes = [32,64,128]
convLayers = [2,3,4]

saveFileName = "trainlog/matrixresults-" + str(int(time.time())) + ".txt"
saveFile = open(saveFileName, "w")
saveFile.write("Layer\tNodes\tDense\tAccuracy\tValidation")
saveFile.close()

for layerSize in layerSizes:
	for convLayer in convLayers:
		for denseLayer in denseLayers:
			runName = "{}-conv-{}-nodes-{}-dense".format(convLayer, layerSize, denseLayer)
			print("")
			print("")
			print(str(round(time.time() - startTime)) + ": ****** Running - " + runName)
			print("")
			print("")

			model = Sequential()

			model.add(Conv2D(layerSize, (3,3), input_shape=imagesTrain.shape[1:]))
			model.add(Activation("relu"))
			model.add(MaxPooling2D(pool_size = (2,2)))

			for layer in range(convLayer - 1):
				model.add(Conv2D(layerSize, (3,3)))
				model.add(Activation("relu"))
				model.add(MaxPooling2D(pool_size = (2,2)))
			
			model.add(Flatten())

			for layer in range(denseLayer):
				model.add(Dense(layerSize))
				model.add(Activation("relu"))

			model.add(Dense(len(categories)))

			# tensorboard = TensorBoard(log_dir = f"scripts/trainlog/{runName}")

			model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer="adam", metrics=["accuracy"])
			history = model.fit(imagesTrain, labelsTrain, epochs=6, batch_size=30, validation_data=(imagesTest, labelsTest)) # , callbacks = [tensorboard]

			saveFile = open(saveFileName, "a")
			saveFile.write(str(layerSize) + "\t" + str(convLayer) + "\t" + str(denseLayer) + "\t" + str(history.history["accuracy"][len(history.history["accuracy"]) - 1]) + "\t" + str(history.history["val_accuracy"][len(history.history["val_accuracy"]) -1]))
			saveFile.close()

			print("")
			print(str(round(time.time() - startTime)) + ": ****** Finished - " + runName + " - accuracy: " + str(history.history["accuracy"][len(history.history["accuracy"]) - 1]) + " - validation: " + str(history.history["val_accuracy"][len(history.history["val_accuracy"]) -1]))

print("complete")
