import requests
import json
import shutil
import os
import time

startTime = time.time()

response = requests.get("http://huntingtonbeach.beynum.com/api/allimages")
files = json.loads(response.text)

print(str(round(time.time() - startTime)) + " - Files to load: " + str(len(files["images"])))

for index, image in enumerate(files["images"]):
    response = requests.get("http://huntingtonbeach.beynum.com/image/" + image, stream = True)

    with open(os.curdir + "/frames/" + image, "wb") as filePointer:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, filePointer)
    
    requests.delete("http://huntingtonbeach.beynum.com/image/" + image)

    if index % 200 == 0:
        print(str(round(time.time() - startTime)) + " - file " + str(index) + " of " + str(len(files["images"])))

print("Completed")
