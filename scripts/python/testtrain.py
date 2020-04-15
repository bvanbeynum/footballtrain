import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import re

startTime = time.time()
files = []
labelsSet = ['start', 'qb', 'player', 'air', 'end']
data = []

frameDir = "./frames"

print(str(round(time.time() - startTime)) + " - Starting")

for file in os.listdir(frameDir):
    fileRE = re.search(r"^([^_]+)_([\d]+)_([^\.]+).jpg", file, flags = re.IGNORECASE)

    if fileRE and fileRE.group(3) != "other":
        files.append({"name": fileRE.group(1), "frame": fileRE.group(2), "category": fileRE.group(3)})
        
        image = cv2.imread(os.path.join(frameDir, file))
		image = cv2.cvtColor(image, code=cv2.COLOR_BGR2RGB)
		data.append([image, ])
