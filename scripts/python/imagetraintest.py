import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.callbacks import TensorBoard
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
import os
import time
import re
import random
import matplotlib.pyplot as plt

startTime = time.time()
categories = ["start", "qb", "player", "air", "end", "other"]
frameDir = "../frames"
files = []
plt.ioff()

validationSplit = 0.3
epocs = 25
fileSize = (192,256)
batchSize = 20
nodes = 32
cnnLayers = 3
denseLayers = 0

saveFileName = "trainlog/imageresults-" + str(int(time.time())) + ".txt"
saveFile = open(saveFileName, "w")
saveFile.write("Images\tResized\tAccuracy\tValidation\n")
saveFile.close()

def buildModel(shape):
	model = Sequential()

	model.add(Conv2D(nodes, (3,3), input_shape=shape))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size = (2,2)))

	for layer in range(cnnLayers - 1):
		model.add(Conv2D(nodes, (3,3)))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size = (2,2)))
		model.add(Dropout(0.2))
	
	model.add(Flatten())

	for denseLayer in range(denseLayers):
		model.add(Dense(nodes))
		model.add(Activation("relu"))
	
	model.add(Dense(len(categories)))

	model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer="adam", metrics=["accuracy"])

	return model

# ************************** Get Files ************************** 

for file in os.listdir(frameDir):
	fileRE = re.search(r"^([^_]+)_([\d]+)_([^\.]+).jpg", file, flags = re.IGNORECASE)

	if fileRE:
		fileName = fileRE.group(1)
		frame = fileRE.group(2)
		category = fileRE.group(3)
		
		existing = list(filter(lambda file: file["name"] == fileName, files))
		if len(existing) > 0:
			existing[0]["frames"].append({ "path": os.path.join(frameDir, file), "category": category })
		else:
			files.append({ "name": fileName, "frames": [{ "path": os.path.join(frameDir, file), "category": category }]})

print(str(round(time.time() - startTime)) + ": Files - " + str(len(files)))

sampleSize = 10
while sampleSize <= len(files):
	images = []
	labels = []

	randomFiles = random.sample(files, sampleSize)
	# randomFiles = files

	# ************************** Resized Files ************************** 

	for file in randomFiles:
		for frame in file["frames"]:
			image = load_img(frame["path"], target_size=fileSize)

			imageArray = img_to_array(image)
			imageArray = imageArray / 255.0
			imageArray = np.array(imageArray)
			
			images.append(imageArray)
			labels.append(categories.index(frame["category"]))

	model = buildModel(imageArray.shape)

	print("")
	print(str(round(time.time() - startTime)) + ": ****** Resized Files - " + str(sampleSize))
	print("")

	imagesTrain, imagesTest, labelsTrain, labelsTest = train_test_split(images, labels, test_size=validationSplit, random_state=0, stratify=labels)
	
	imagesTrain = np.array(imagesTrain)
	imagesTest = np.array(imagesTest)
	labelsTrain = np.array(labelsTrain)
	labelsTest = np.array(labelsTest)

	results = model.fit(imagesTrain, labelsTrain, epochs=epocs, batch_size=batchSize, validation_data=(imagesTest, labelsTest))

	predictions = model.predict(imagesTest)
	matrix = metrics.confusion_matrix(labelsTest, predictions.argmax(axis=1))
	
	metrics.ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=categories).plot()
	plt.savefig("trainlog/imagepic_" + str(sampleSize) + "-resize-" + str(int(time.time())) + ".png", bbox_inches="tight")
	plt.close()

	saveFile = open(saveFileName, "a")
	saveFile.write(str(sampleSize) + "\t1\t" + str(results.history["accuracy"][len(results.history["accuracy"]) - 1]) + "\t" + str(results.history["val_accuracy"][len(results.history["val_accuracy"]) -1]) + "\n")
	saveFile.close()

	print("")
	print(str(round(time.time() - startTime)) + ": ****** Finished resized - " + str(sampleSize) + " - accuracy: " + str(results.history["accuracy"][len(results.history["accuracy"]) - 1]) + " - validation: " + str(results.history["val_accuracy"][len(results.history["val_accuracy"]) -1]))

	# ************************** Full Size Files ************************** 
	images = []
	labels = []

	for file in randomFiles:
		for frame in file["frames"]:
			image = load_img(frame["path"])

			imageArray = img_to_array(image)
			imageArray = imageArray / 255.0
			imageArray = np.array(imageArray)
			
			images.append(imageArray)
			labels.append(categories.index(frame["category"]))

	model = buildModel(imageArray.shape)

	print("")
	print(str(round(time.time() - startTime)) + ": ****** Full Size Files - " + str(sampleSize))
	print("")

	imagesTrain, imagesTest, labelsTrain, labelsTest = train_test_split(images, labels, test_size=validationSplit, random_state=0, stratify=labels)
	
	imagesTrain = np.array(imagesTrain)
	imagesTest = np.array(imagesTest)
	labelsTrain = np.array(labelsTrain)
	labelsTest = np.array(labelsTest)

	results = model.fit(imagesTrain, labelsTrain, epochs=epocs, batch_size=batchSize, validation_data=(imagesTest, labelsTest))

	predictions = model.predict(imagesTest)
	matrix = metrics.confusion_matrix(labelsTest, predictions.argmax(axis=1))
	
	metrics.ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=categories).plot()
	plt.savefig("trainlog/imagepic_" + str(len(images)) + "-full-" + str(int(time.time())) + ".png", bbox_inches="tight")
	plt.close()

	saveFile = open(saveFileName, "a")
	saveFile.write(str(sampleSize) + "\t0\t" + str(results.history["accuracy"][len(results.history["accuracy"]) - 1]) + "\t" + str(results.history["val_accuracy"][len(results.history["val_accuracy"]) -1]))
	saveFile.close()

	print("")
	print(str(round(time.time() - startTime)) + ": ****** Finished full sized - " + str(sampleSize) + " - accuracy: " + str(results.history["accuracy"][len(results.history["accuracy"]) - 1]) + " - validation: " + str(results.history["val_accuracy"][len(results.history["val_accuracy"]) -1]))

	sampleSize += 10
	
print("done")