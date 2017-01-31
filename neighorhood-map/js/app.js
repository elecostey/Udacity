var map;
//Our local Database
var markers = [{
	title: 'Archaeological Museum in Zagreb',
	lat: 45.810904,
	lng: 15.977325,
	address: 'Trg Nikole Šubića Zrinskog 19',
	shouldDisplay: true,
	id: 'location0',
	visible: ko.observable(true)
}, {
	title: 'Mimara Museum',
	lat: 45.808195,
	lng: 15.967236,
	address: 'Rooseveltov trg 5',
	shouldDisplay: true,
	id: 'location1',
	visible: ko.observable(true)
}, {
	title: 'Croatian National Theatre in Zagreb',
	lat: 45.809391,
	lng: 15.970009,
	address: 'Trg maršala Tita 15',
	shouldDisplay: true,
	id: 'location2',
	visible: ko.observable(true)
}, {
	title: 'Art Pavilion, Zagreb',
	lat: 45.807217,
	lng: 15.978617,
	address: 'Trg kralja Tomislava 22',
	shouldDisplay: true,
	id: 'location3',
	visible: ko.observable(true)
}, {
	title: 'Zagreb Cathedral',
	lat: 45.814508,
	lng: 15.979822,
	address: 'Kaptol ul. 31',
	shouldDisplay: true,
	id: 'location4',
	visible: ko.observable(true)
}, {
	title: 'Croatian Academy of Sciences and Arts',
	lat: 45.809120,
	lng: 15.978554,
	address: 'Trg Nikole Šubića Zrinskog 11',
	shouldDisplay: true,
	id: 'location5',
	visible: ko.observable(true)
}, {
	title: 'Nikola Šubić Zrinski Square',
	lat: 45.810420,
	lng: 15.978349,
	address: 'Trg Nikole Šubića Zrinskog 6',
	shouldDisplay: true,
	id: 'location6',
	visible: ko.observable(true)
}, {
	title: 'Zagreb Botanical Garden',
	lat: 45.804809,
	lng: 15.971822,
	address: 'Mihanovićeva ul. 32',
	shouldDisplay: true,
	id: 'location7',
	visible: ko.observable(true)
}];

function initProject() {
	var script = document.createElement('script');
	script.type = 'text/javascript';
	script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBuR9YR4fwGm8rOm69uNKvF5wYKKJrt6U0&callback=loadMap';
	document.body.appendChild(script);
}
window.onload = initProject;

function loadMap() {
	var mapOptions = {
		zoom: 15,
		center: new google.maps.LatLng(45.811695, 15.975037),
		mapTypeControl: false
	};
	map = new google.maps.Map(document.getElementById('map'), mapOptions);
	addMarker(markers);
	drawMarkersOnMap();
}

function drawMarkersOnMap() {
	for (var i = 0; i < markers.length; i++) {
		if (markers[i].shouldDisplay === true) {
			markers[i].mapMarkerObject.setMap(map);
		} else {
			markers[i].mapMarkerObject.setMap(null);
		}
	}
}

function addMarker(location) {
	for (i = 0; i < location.length; i++) {
		location[i].mapMarkerObject = new google.maps.Marker({
			position: new google.maps.LatLng(location[i].lat, location[i].lng),
			map: map,
			icon: {
				url: 'images/marker.png',
				scaledSize: new google.maps.Size(25, 40),
			},
			shape: {
				coords: [1, 25, -40, -25, 1],
				type: 'poly'
			},
			title: location[i].title,
			description: location[i].description
		});
		location[i].contentString = '<strong>' + location[i].title + '</strong>';
		var infoWindow = new google.maps.InfoWindow({
			maxWidth: 250,
			content: markers[i].contentString
		});
		// Click marker to view infoWindow
		// zoom in and center location on click
		// async load of Wikipedia description and url for given location
		new google.maps.event.addListener(location[i].mapMarkerObject, 'click', (function(marker, i) {
			return function() {
				infoWindow.setContent(location[i].contentString);
				infoWindow.open(map, this);
				map.setZoom(16);
				map.setCenter(marker.getPosition());
				location[i].picBoolTest = true;
				var wikiUrl = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + location[i].title + '&format=json&callback=wikiCallback';
				var wikiRequestTimeout = setTimeout(function() {
					infoWindow.setContent("failed to get wikipedia resources");
				}, 3500);
				$.ajax({
					url: wikiUrl,
					dataType: "jsonp",
					success: function(response) {
						var articleList = response[1];
						var descriptionList = response[2];
						var urlList = response[3];
						for (var i = 0; i < articleList.length; i++) {
							articleStr = articleList[i];
							articleDesc = descriptionList[i]
							articleUrl = urlList[i]
							infoWindow.setContent('<strong>' + articleList + '</strong>' + '<br>' + '<br>' + articleDesc + '<br>' + '<br>' + '<a href="' + articleUrl + '" target="_blank">' + "view on Wikipedia" + '</a>');
						};
						clearTimeout(wikiRequestTimeout);
					}
				});
			};
		})(location[i].mapMarkerObject, i));
		// zoom in and center location on click
		// async load of Wikipedia description and url for given location
		var filterLocation = $('#location' + i);
		var windowWidth = $(window).width();
		filterLocation.click((function(marker, i) {
			return function() {
				console.log("clicked:" + marker.title);
				infoWindow.setContent(location[i].contentString);
				infoWindow.open(map, marker);
				if ($(window).width() < 500) {
					closeNav();
				} else {
					openNav();
				}
				map.setZoom(16);
				map.setCenter(marker.getPosition());
				location[i].picBoolTest = true;
				var wikiUrl = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + location[i].title + '&format=json&callback=wikiCallback';
				var wikiRequestTimeout = setTimeout(function() {
					infoWindow.setContent("failed to get wikipedia resources");
				}, 3500);
				$.ajax({
					url: wikiUrl,
					dataType: "jsonp",
					success: function(response) {
						var articleList = response[1];
						var descriptionList = response[2];
						var urlList = response[3];
						for (var i = 0; i < articleList.length; i++) {
							articleStr = articleList[i];
							articleDesc = descriptionList[i]
							articleUrl = urlList[i]
							infoWindow.setContent('<strong>' + articleList + '</strong>' + '<br>' + '<br>' + articleDesc + '<br>' + '<br>' + '<a href="' + articleUrl + '" target="_blank">' + "view on Wikipedia" + '</a>');
						};
						clearTimeout(wikiRequestTimeout);
					}
				});
			};
		})(location[i].mapMarkerObject, i));
	}
}
var viewModel = {
	query: ko.observable(''),
};
viewModel.markers = ko.dependentObservable(function() {
	var self = this;
	var search = self.query().toLowerCase();
	return ko.utils.arrayFilter(markers, function(marker) {
		if (marker.title.toLowerCase().indexOf(search) >= 0) {
			marker.shouldDisplay = true;
			return marker.visible(true);
		} else {
			marker.shouldDisplay = false;
			drawMarkersOnMap();
			return marker.visible(false);
		}
	});
}, viewModel);
ko.applyBindings(viewModel);
//Our dynamic filter implementation runs after each keystroke
$("#input").keyup(function() {
	drawMarkersOnMap();
});

function openNav() {
	document.getElementById("mySidenav").style.width = "320px";
	document.getElementById("pushed").style.zIndex = "10";
	document.getElementById("pushed").style.fontSize = "28px";
	document.getElementById("search-icon").style.display = "none";
}

function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
	document.getElementById("pushed").style.marginLeft = "0";
	document.getElementById("pushed").style.fontSize = "36px";
	document.getElementById("search-icon").style.display = "block";
}