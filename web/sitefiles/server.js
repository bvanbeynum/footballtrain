// Setup =======================================================================

var express = require("express");
var path = require("path");
var fs = require("fs");
var busboy = require("connect-busboy");
var bodyParser = require("body-parser");
var app = express();
var port = process.env.PORT || 8080;

// Config =======================================================================

app.set("x-powered-by", false);
app.set("root", __dirname);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(busboy()); 

// Routes =======================================================================

app.post("/uploadvideo", (request, response) => {
	
	request.busboy.on("file", (fieldName, file, fileName) => {
		file.pipe(fs.createWriteStream(path.join(app.get("root"), "server/video/" + fileName)));
	});
	request.busboy.on("finish", () => {
		response.status(200).json({status: "ok"});
	});
	
	request.pipe(request.busboy);
});

app.post("/api/imagecategory", (request, response) => {
	var file = request.body.image, 
		newCategory = request.body.category,
		newFile = file.replace(/_category/i, "_" + newCategory);
	
	fs.rename(path.join(app.get("root"), "server/frame/" + file), path.join(app.get("root"), "server/frame/" + newFile), (error) => {
		if (error) {
			response.status(501).json({ error: error.message });
		}
		else {
			response.status(200).json({ status: "ok" });
		}
	});
});

app.get("/api/nextimage", (request, response) => {
	
	fs.readdir(path.join(app.get("root"), "server/frame"), (error, files) => {
		
		var match, images = [], complete = 0;
		for (var file of files) {
			match = String(file).match(/^([^_]+)_([\d]+)_([^\.]+).jpg/i);
			
			if (match && match[3] == "category") {
				images.push({file: file, frame: match[2], name: match[1]});
			}
			else {
				complete++;
			}
		}
		
		images.sort((prev, next) => {
			if (prev.name < next.name) {
				return -1;
			}
			else if (prev.name > next.name) {
				return 1;
			}
			else if (+prev.frame < +next.frame) {
				return -1;
			}
			else {
				return 1;
			}
		});
		
		if (images.length > 0) {
			response.status(200).json({ image: images[0].file, complete: complete, remain: images.length });
		}
		else {
			response.status(404).send("No images found");
		}
	});
});

app.get("/api/allimages", (request, response) => {
	
	fs.readdir(path.join(app.get("root"), "server/frame"), (error, files) => {
		
		var match, images = [];
		for (var file of files) {
			match = String(file).match(/^([^_]+)_([\d]+)_([^\.]+).jpg/i);
			
			if (match && match[3] != "category") {
				images.push({file: file, frame: match[2], name: match[1]});
			}
		}
		
		images.sort((prev, next) => {
			if (prev.name < next.name) {
				return -1;
			}
			else if (prev.name > next.name) {
				return 1;
			}
			else if (+prev.frame < +next.frame) {
				return -1;
			}
			else {
				return 1;
			}
		});
		
		response.status(200).json({ images: images.map(image => image.file)});
	});
});

app.delete("/image/*.jpg", (request, response) => {
	fs.stat(path.join(app.get("root"), "/server/frame/" + request.url.substring(7, request.url.length)), (error) => {
		if (error) {
			response.status(404).send("File not found");
		}
		else {
			fs.unlink(path.join(app.get("root"), "/server/frame/" + request.url.substring(7, request.url.length)), (error) => {
				if (error) {
					console.log(error);
					response.status(501).json({ error: error.message });
				}
				else {
					response.status(200).send("ok");
				}
			});
		}
	});
	
});

app.get("/", (request, response) => {
	response.sendFile("/client/index.html", { root: app.get("root") });
});

app.get("/image/*.jpg", (request, response) => {
	response.sendFile("/server/frame/" + request.url.substring(7, request.url.length), { root: app.get("root") });
});

app.get("/index.js", function(request, response) {
	response.sendFile("/client/index.js", { root: app.get("root") });
});

app.get("/tagging", (request, response) => {
	response.sendFile("/client/tagging.html", { root: app.get("root") });
});

app.get("/tagging.js", function(request, response) {
	response.sendFile("/client/tagging.js", { root: app.get("root") });
});

app.get("*", (request, response) => {
	response.status(404).send("Invalid path: " + request.path);
	response.end();
});

// listen (start app with node server.js) ======================================

app.listen(port);
console.log("App listening on port " + port);
