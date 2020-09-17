import os
import re

frameDir = "./files/frame"
files = {}

categories = {
	"start": 1,
	"qb": 2,
	"air": 3,
	"player": 3
}

# files["test1"] = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
# files["test2"] = [{"a": 5, "b": 6}, {"a": 7, "b": 8}]

# for index, (file, frames) in enumerate(files.items()):
# 	for index, frame in enumerate(frames):
# 		print(frame)

for index, file in enumerate(os.listdir(frameDir)):
	fileRE = re.search(r"^([^_]+)_([\d]+)_([^\.]+).jpg", file, flags = re.IGNORECASE)
	
	if fileRE and fileRE.group(3) != "category":
		fileName = fileRE.group(1)
		frame = fileRE.group(2)
		category = fileRE.group(3)
		
		if fileName in files:
			files[fileName].append({"frame": fileRE.group(2), "category": fileRE.group(3)})
		else:
			files[fileName] = [{"frame": fileRE.group(2), "category": fileRE.group(3)}]

for index, (file, frames) in enumerate(files.items()):
	frames = sorted(frames, key = lambda k: int(k["frame"]))
	maxCategory = 1
	prevFrame = None
	
	for index, frame in enumerate(frames):
		if frame["category"] in ["missing", "ground"]:
			continue
		
		elif categories[frame["category"]] > maxCategory:
			maxCategory = categories[frame["category"]]
			
		elif categories[frame["category"]] < maxCategory:
			print("error" + str(categories[prevFrame["category"]]) + " / " + str(categories[frame["category"]]) + " - " + str(maxCategory))
			print("\thttp://huntingtonbeach.beynum.com/image/" + file + "_" + prevFrame["frame"] + "_" + prevFrame["category"] + ".jpg")
			print("\thttp://huntingtonbeach.beynum.com/image/" + file + "_" + frame["frame"] + "_" + frame["category"] + ".jpg")
			print("\tmv /home/bvanbeynum/footballtrain/web/sitefiles/server/frame/" + file + "_" + prevFrame["frame"] + "_" + prevFrame["category"] + ".jpg /home/bvanbeynum/footballtrain/web/sitefiles/server/frame/" + file + "_" + prevFrame["frame"] + "_" + frame["category"] + ".jpg")
			
			maxCategory = categories[frame["category"]]
		
		prevFrame = frame
		