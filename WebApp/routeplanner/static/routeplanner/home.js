// click function for div item
$(document).ready(function() {
    $( "#sidebar" ).load( "/journey #content" );
    $('.nav_item').click(function(e) {  
        // Get the name of tab on the navbar that was clicked
        var nav_id = $(this).attr('id');
        console.log(nav_id);

        // Update sidebar content with appropriate html
        $("#sidebar").load("/" + nav_id + " #content");
    });

    $('#test').click(function(e) {  
        console.log('test');
    });
});

// Initialize and add the map
var mymap = L.map('map').setView([53.3482, -6.2641], 12);
// Set map hight 
$("#map").height($(window).height()-80);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoib2hteWhhcHB5IiwiYSI6ImNrYjdyaWg0cDA0bXMycXFyNzgxdmkyN3kifQ.gcq3O8-AveWKXNS5TUGL_g'
}).addTo(mymap);


