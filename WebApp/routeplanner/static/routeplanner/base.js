// click function for div item
$(document).ready(function() {
    $('.nav_item').click(function(e) {  
        var id = $(this).attr('id');
        console.log(id);

        // change content when nav item clicked
        if (id == "journey"){
            $( "#content" ).load( "home.html" );
            // $( "#content" ).load( "../../tempeletes/routeplanner/home.html" );
        };
    });
});

// Initialize and add the map
var mymap = L.map('map').setView([53.3482, -6.2641], 12);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoib2hteWhhcHB5IiwiYSI6ImNrYjdyaWg0cDA0bXMycXFyNzgxdmkyN3kifQ.gcq3O8-AveWKXNS5TUGL_g'
}).addTo(mymap);

