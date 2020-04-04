import requests
import json
import shutil
import os

response = requests.get("http://dev.beynum.com:8080/api/allimages")
files = json.loads(response.text)

for image in files["images"]:
    response = requests.get("http://dev.beynum.com:8080/image/" + image, stream = True)

    with open(os.curdir + "/frames/complete/" + image, "wb") as filePointer:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, filePointer)
    
    requests.delete("http://dev.beynum.com:8080/image/" + image)

print("Completed")
