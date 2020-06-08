
var initMap = () => {
    this.map = new google.maps.Map(
        document.getElementById('map'), {
            zoom: 15,
            center: {lat: 53.3568, lng: -6.26814},  // Blessington Street station
            fullscreenControl: false
        });

    this.infowindow = new google.maps.InfoWindow();

    // Try HTML5 geolocation.
    //Setting and Scrolling user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        // The marker, positioned at user location
        var marker = new google.maps.Marker({position: pos, map: map});
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, infowindow, map.getCenter());
      });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infowindow, map.getCenter());
    }

};