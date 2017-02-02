'use strict';

function loadMap() {

    var viewModel = function () {
        var self = this;
        self.markers = new ko.observableArray();
        self.location = ko.observableArray();
        self.contentString = ko.observable('');
        self.searchFilter = ko.observable('');

        // Google map setup to display Zagreb/Croatia
        self.map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            mapTypeControl: false,
            center: {
                lat: 45.811695,
                lng: 15.975037
            }
        });

        self.InfoMarker = new google.maps.InfoWindow({
            maxWidth: 250,
            content: self.contentString()
        });

        // Querying Wikipedia for description and url based on wiki id 
        self.queryWikipedia = function (wikiId) {

            var wikiUrl = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + wikiId + '&format=json&callback=wikiCallback';

            var selectedMarker = null;
            self.markers().forEach(function (currentmarker) {
                if (currentmarker.wiki_id === wikiId) {
                    selectedMarker = currentmarker;
                }
            });

            $.ajax({
                url: wikiUrl,
                dataType: 'jsonp',
                timeout: 2500,
                success: function (response) {
                    var articleList = response[1];
                    var descriptionList = response[2];
                    var urlList = response[3];
                    console.log(urlList[0]);

                    self.InfoMarker.setContent('<strong>' + articleList[0] + '</strong>' + '<br>' + '<br>' + descriptionList[0] + '<br>' + '<br>' + '<a href="' + urlList[0] + '" target="_blank">' + "view on Wikipedia" + '</a>');

                    if (self.InfoMarker != null) {
                        self.InfoMarker.close();
                    }
                    // zoom in and center location on side panel click
                    if ($(window).width() < 500) {
						closeNav();
					} else {
						openNav();
					}
                    self.InfoMarker.open(self.map, selectedMarker);
                    self.map.setZoom(16);
                    self.map.setCenter(selectedMarker.getPosition());
                    bounceMapMarker(selectedMarker, google.maps.Animation.BOUNCE);

                }, error: function () {
                    // will fire when timeout is reached
                    self.InfoMarker.setContent('<strong>failed to get wikipedia resources</strong>');

                    if (self.InfoMarker != null) {
                        self.InfoMarker.close();
                    }
                    self.InfoMarker.open(self.map, selectedMarker);
                }
            });
        };

        //Create our locations based on title, address, lattitude, longitude and wiki_id
        self.generateLocation = function (title, address, latitude, longitude, wiki_id) {
            var location = {
                position: new google.maps.LatLng(latitude, longitude),
                title: title,
                address: address,
                visible: true,
                map: self.map,
                wiki_id: wiki_id
            };

            // Create our map marker objects based on the location object and push to marker observable array
            var markerObject = new google.maps.Marker(location);
            self.markers.push(markerObject);
            markerObject.setAnimation(null);
            markerObject.setIcon('images/marker.png');
            // Click marker to view infoWindow
            markerObject.addListener('click', function () {
                self.queryWikipedia(this.wiki_id);
                // zoom in and center location on side panel click
                self.InfoMarker.open(self.map, this);
                self.map.setZoom(16);
                self.map.setCenter(this.getPosition());
                bounceMapMarker(this, google.maps.Animation.BOUNCE);
            });

            // Return the location object
            return location;
        };

        self.coordinates = [
            new self.generateLocation('Archaeological Museum', 'Trg Nikole Šubića Zrinskog 19', 45.810904, 15.977325, 'Archaeological Museum in Zagreb'),
            new self.generateLocation('Mimara Museum', 'Rooseveltov trg 5', 45.808195, 15.967236, 'Mimara Museum'),
            new self.generateLocation('Croatian National Theatre', 'Trg maršala Tita 15', 45.809391, 15.970009, 'Croatian National Theatre in Zagreb'),
            new self.generateLocation('Art Pavilion', 'Trg kralja Tomislava 22', 45.807217, 15.978617, 'Art Pavilion, Zagreb'),
            new self.generateLocation('Zagreb Cathedral', 'Kaptol ul. 31', 45.814508, 15.979822, 'Zagreb Cathedral'),
            new self.generateLocation('Croatian Academy of Sciences and Arts', 'Trg Nikole Šubića Zrinskog 11', 45.809120, 15.978554, 'Croatian Academy of Sciences and Arts'),
            new self.generateLocation('Nikola Šubić Zrinski Square', 'Trg Nikole Šubića Zrinskog 6', 45.810420, 15.978349, 'Nikola Šubić Zrinski Square'),
            new self.generateLocation('Zagreb Botanical Garden', 'Mihanovićeva ul. 32', 45.804809, 15.971822, 'Zagreb Botanical Garden'),
        ];

        // Our dynamic filter implementation runs after each keystroke
        // updating both the side panel and the markers on the map
        self.searchFilter.subscribe(function (inputValue) {
            inputValue = inputValue.toLowerCase();

            var needToChange = false;
            ko.utils.arrayForEach(self.markers(), function (marker) {
                var text = marker.title.toLowerCase();

                if (text.search(inputValue) === -1) {

                    if (marker.getVisible() === true) {
                        needToChange = true;

                        if (self.InfoMarker != null) {
                            self.InfoMarker.close();
                        }
                    }
                    marker.setVisible(false);
                } else {
                    if (marker.getVisible() === false) {
                        needToChange = true;
                    }
                    marker.setVisible(true);
                }

            });
            if (needToChange === true) {
                var data = self.markers().slice(0);
                self.markers([]);
                self.markers(data);
            }
        });
    };

    ko.applyBindings(new viewModel());
}
// error handling for google map API
function mapError() {
    $('#map').text('Google Map could not be loaded');
};

function bounceMapMarker(marker, animation) {
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(animation);
        setTimeout(function () {
            marker.setAnimation(null);
        }, 1400);
    }
}

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