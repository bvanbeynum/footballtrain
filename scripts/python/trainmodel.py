import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from tensorflow.keras.callbacks import TensorBoard
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
categories = ["start", "qb", "player", "air", "ground", "missing"]
frameDir = "../frames/run"
files = []
plt.ioff()
modelNumber = str(int(time.time()))

framesCount = 100
validationSplit = 0.3
epocs = 12
fileSize = (480,640)
batchSize = 60
nodes = 32
cnnLayers = 3
denseLayers = 0

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

images = []
labels = []

# randomFiles = random.sample(files, framesCount)
randomFiles = files

# ************************** Training Data ************************** 

for file in randomFiles:
	for frame in file["frames"]:
		image = load_img(frame["path"], target_size=fileSize)

		imageArray = img_to_array(image)
		imageArray = imageArray / 255.0
		imageArray = np.array(imageArray)
		
		images.append(imageArray)
		labels.append(categories.index(frame["category"]))

imagesTrain, imagesTest, labelsTrain, labelsTest = train_test_split(images, labels, test_size=validationSplit, random_state=0, stratify=labels)

imagesTrain = np.array(imagesTrain)
imagesTest = np.array(imagesTest)
labelsTrain = np.array(labelsTrain)
labelsTest = np.array(labelsTest)

labelsTrainCategorical = keras.utils.to_categorical(labelsTrain)
labelsTestCategorical = keras.utils.to_categorical(labelsTest)

# ************************** Build Model ************************** 

model = Sequential()

model.add(Conv2D(nodes, (3,3), activation="relu", input_shape=imagesTrain.shape[1:]))
model.add(MaxPooling2D(pool_size = (2,2)))

for layer in range(cnnLayers - 1):
	model.add(Conv2D(nodes, (3,3), activation="relu"))
	model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())

for denseLayer in range(denseLayers):
	model.add(Dense(nodes), activation="relu")
	model.add(Dropout(0.2))

model.add(Flatten())

model.add(Dense(len(categories), activation="softmax"))

tensorboard = TensorBoard(log_dir=f"trainlog\model_{modelNumber}")
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
results = model.fit(imagesTrain, labelsTrainCategorical, epochs=epocs, batch_size=batchSize, validation_data=(imagesTest, labelsTestCategorical), callbacks=[tensorboard])

predictions = model.predict(imagesTest)
matrix = metrics.confusion_matrix(labelsTestCategorical.argmax(axis=1), predictions.argmax(axis=1))

metrics.ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=categories).plot()
plt.savefig(f"trainlog\model_{modelNumber}\matrix.png", bbox_inches="tight")
plt.close()

model.save(f"trainlog\model_{modelNumber}\model")

print("")
print(str(round(time.time() - startTime)) + ": ****** Completed - accuracy: " + str(results.history["accuracy"][len(results.history["accuracy"]) - 1]) + " - validation: " + str(results.history["val_accuracy"][len(results.history["val_accuracy"]) -1]))
