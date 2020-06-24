// click function for div item
$(document).ready(function() {

    $( "#sidebar" ).load( "/journey #content");

    $('.nav_item').click(function(e) {  
        // Get the name of tab on the navbar that was clicked
        var nav_id = $(this).attr('id');
        console.log(nav_id);

        // Update sidebar content with appropriate html
        $("#sidebar").load("/" + nav_id + "#script");
    });
    initMap();
});


//centreLocation: default value is Dublin city centre,
//If user allow location access, than set value to user location
var centreLocation = [53.3482, -6.2641]

// Initialize and add the map
var map = L.map('map').setView(centreLocation, 14);


function initMap(){

    // Set map hight 
    $("#map").height($(window).height()-80);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoib2hteWhhcHB5IiwiYSI6ImNrYjdyaWg0cDA0bXMycXFyNzgxdmkyN3kifQ.gcq3O8-AveWKXNS5TUGL_g'
    }).addTo(map);

    map.locate({setView: true, watch: true});

    var onLocationFound = function(e){
        L.marker(e.latlng)
        .addTo(map)
        .bindPopup("You are here!")
        .openPopup();
        centreLocation = e.latlng;
        map.setView(e.latlng, 14);
    };


    map.on('locationfound', onLocationFound);
}







