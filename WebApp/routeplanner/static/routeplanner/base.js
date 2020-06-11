// click function for div item
$(document).ready(function() {
    $('.nav_item').click(function(e) {  
        var id = $(this).attr('id');
        console.log(id);

        // change content when nav item clicked
        if (id == "journey"){
            // get() will send a request to django the URL you give it as the first arg, you'll need to set up the urls.py and a views.py in django so that
            // it returns the appropriate html
            // That html will then be returned  as "data" in the function belows
            $.get( "/journey", function( data ) {
                $("#content").html(data)
            } );
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

