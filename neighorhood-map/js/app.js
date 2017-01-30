var map;
      function initMap() {
        var trnsko = {lat: 45.773113, lng: 15.964594};
        var caffeBarPepper = {lat: 45.772963, lng: 15.964991};
        map = new google.maps.Map(document.getElementById('map'), {
          center: trnsko,
          zoom: 15,
          disableDefaultUI: true
        });

        var marker = new google.maps.Marker({
          position: caffeBarPepper,
          map: map,
          title: 'Caffe Bar Pepper'
        });

        var contentString = '<div id="content">'+
          '<div id="siteNotice">'+
          '</div>'+
          '<h2 id="firstHeading" class="firstHeading">Caffe Bar Pepper</h2>'+
          '<div id="bodyContent">'+
          '<h4>Pizzeria</h4>'+
          '<p>Trnsko ul. 29C</p>'+
          '<p>10000, Zagreb</p>'+
          '<p>Croatia</p>'+
          '</div>'+
          '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
          });

        marker.addListener('click', function() {
            infowindow.open(map, marker);
          });
      }

/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
    document.getElementById("pushed").style.marginLeft = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("pushed").style.marginLeft = "0";
}