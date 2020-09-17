/* global angular */

var log = {},
	trainingApp = angular.module("trainingApp", []);

trainingApp.controller("trainingCtl", ($scope, $http, $window) => {
	
	log.scope = $scope;
	log.http = $http;
	
	$scope.categories = ["start", "qb", "air", "player", "ground", "missing"];
	$scope.showNewCategory = false;
	$scope.currentImage = null;
	
	$scope.upload = { queue: [], error: [], complete: [] };
	
	$http({url: "/api/nextimage"}).then((response) => {
		$scope.currentImage = response.data.image;
		$scope.imagesRemain = response.data.remain;
		$scope.imagesComplete = response.data.complete;
		
		$scope.frame = $scope.currentImage.match(/_([^_]+)_/i)[1];
	}, (error) => {
		
		if (error.status == 404) {
			$scope.currentImage = null;
		}
		else {
			console.log(error);
			$scope.showError(error);
		}
		
	});
	
	$scope.saveCategory = () => {
		$scope.categories.push($scope.newCategory);
		$scope.showNewCategory = false;
		$scope.newCategory = null;
	};
	
	$scope.selectCategory = (category) => {
		$http({url: "/api/imagecategory", method: "post", data: { image: $scope.currentImage, category: category }}).then((response) => {
			
			// Get next image
			$http({url: "/api/nextimage"}).then((response) => {
				$scope.currentImage = response.data.image;
				$scope.imagesRemain = response.data.remain;
				$scope.imagesComplete = response.data.complete;
				
				$scope.frame = $scope.currentImage.match(/_([^_]+)_/i)[1];
			}, (error) => {
				
				if (error.status == 404) {
					$scope.currentImage = null;
				}
				else {
					console.log(error);
					$scope.showError(error);
				}
				
			});
			
		}, (error) => {
			console.log(error);
			$scope.showError(error);
		});
	};
	
	$scope.showError = (message) => {
		$scope.errorMessage = message;
		$scope.showError = true;
		
		setTimeout(() => {
			$scope.errorMessage = null;
			$scope.showError = false;
			$scope.$apply();
		}, 3000);
	};
	
	angular.element($window).on("dragenter", (event) => {
		event.stopPropagation();
		event.preventDefault();
		
		$scope.$apply(function () {
			$scope.isOver = true;
		});
	});
	
	$scope.dragOver = (event) => {
		event.stopPropagation();
		event.preventDefault();
	};
	
	$scope.dragLeave = (event) => {
		event.stopPropagation();
		event.preventDefault();
		
		$scope.$apply(function () {
			$scope.isOver = false;
		});
	};
	
	$scope.drop = (event) => {
		event.stopPropagation();
		event.preventDefault();
		
		$scope.$apply(function () {
			$scope.isOver = false;
		});
		
		var files = event.dataTransfer.files;
		log.files = files;
		
		console.log("dropped: " + files.length);
		
		$scope.upload.queue = Array.from(files);
		$scope.upload.error = [];
		$scope.upload.complete = [];
		
		uploadVideo();
		
	};
	
	function uploadVideo() {
		var formUpload = new FormData();
		formUpload.append("file", $scope.upload.queue[0]);
		
		$http({url: "/uploadvideo", method: "post", headers: { "Content-Type": undefined }, data: formUpload }).then(
			function (response) {
				var uploadedFile = $scope.upload.queue.shift();
				$scope.upload.complete.push(uploadedFile);
				
				if ($scope.upload.queue.length > 0) {
					uploadVideo();
				}
			}, function (error) {
				console.log(error);
				
				var uploadedFile = $scope.upload.queue.shift();
				$scope.upload.error.push(uploadedFile);
				
				if ($scope.upload.queue.length > 0) {
					uploadVideo();
				}
			});
	}
	
});

var dragObject = { active: false, initial: { x: 0, y: 0 }, current: { x: 0, y:0 }, offset: { x: 0, y: 0 } };

window.onload = () => {
	dragObject.object = document.getElementById("dragHTML");
};

function dragStart(event) {
	if (event.type == "touchstart") {
		dragObject.initial.x = event.touches[0].clientX - dragObject.offset.x;
		dragObject.initial.y = event.touches[0].clientY - dragObject.offset.y;
	}
	else {
		dragObject.initial.x = event.clientX - dragObject.offset.x;
		dragObject.initial.y = event.clientY - dragObject.offset.y;
	}
	
	dragObject.active = true;
}

function dragEnd(event) {
	dragObject.initial.x = dragObject.current.x;
	dragObject.initial.y = dragObject.current.y;
	
	dragObject.active = false;
}

function drag(event) {
	if (dragObject.active) {
		event.preventDefault();
		
		if (event.type == "touchmove") {
			dragObject.current.y = event.touches[0].clientY - dragObject.initial.y;
		}
		else {
			dragObject.current.y = event.clientY - dragObject.initial.y;
		}
		
		dragObject.offset.x = dragObject.current.x;
		dragObject.offset.y = dragObject.current.y;
		
		dragObject.object.style.transform = "translate3d(" + dragObject.current.x + "px, " + dragObject.current.y + "px, 0)";
	}
}