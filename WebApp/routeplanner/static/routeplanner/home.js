const RESP_WINDOW_SIZE = 768

// Code in this block will be run one the page is loaded in the browser
$(document).ready(function () {

    // Load the journey UI content by default
    loadSideBarContent("journey");

    // on click function for nav-items
    $('.nav_item').click(function () {

        // Get the name of tab on the navbar that was clicked
        var nav_id = $(this).attr('id');

        // Update sidebar content with appropriate html

        loadSideBarContent(nav_id)
    });

    // on click function for bottom-nav-items
    // This is slightly different to the side-bar nav
    // as it also shows and hides the map
    $('.bottom_nav_item').click(function () {
        // Get the name of tab on the navbar that was clicked
        var nav_id = $(this).attr('id');

        // remove "bottom" from the nav-id
        nav_id = nav_id.split("-")[1];

        // Show the map
        if (nav_id === "showmap") {
            $("#sidebar, #resp-sidebar-menu").hide();
            $("#map, #resp-map-menu").show();

            // Leaflet needs this to update the map display
            // after being hidden
            map.invalidateSize();
        
        // Hide the map
        } else if (nav_id === "hidemap") {
            $("#sidebar, #resp-sidebar-menu").show();
            $("#map, #resp-map-menu").hide();

        // Otherwise load the appropriate UI
        } else {
            loadSideBarContent(nav_id)
        }

    });
    initMap();
});


//centreLocation: default value is Dublin city centre,
//If user allow location access, than set value to user location
var centreLocation = [53.3482, -6.2641]

// Initialize and add the map
var map = L.map('map').setView(centreLocation, 14);
//init layer for storeing all stop markers
var stopsLayer = L.layerGroup().addTo(map);
//init layer for storeing journey 
var journeyLayer = L.layerGroup().addTo(map);



function clearElementsInLayers(){
    //clear all the markers in the layer
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();
}



function initMap(){

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


var MapUIControl = (function () {

    return {
        hidemap: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                $("#map").animate({ height: "0px" }, 500, () => {
                    $("#map").hide();
                    $("#mobile-show-content").hide();
                });
            }
        },

        halfscreen: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                $(".sidebar_header").hide();
                $("#mobile-show-content").hide();
                $('#sidebar').fadeIn(10);
                $("#map").show()
                    .animate({ height: "125px" }, 500, () => map.invalidateSize(false));
            }
        },

        fullscreen: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                $(".sidebar_header").hide();

                var newHeight = $(window).height() - 80 - 60 - 50;
                $('#sidebar').fadeOut(10);
                $("#mobile-show-content").show();
                $("#map").show()
                    .animate({ height: newHeight }, 500, () => map.invalidateSize(false));
            }
        },
        reset: function () {
            $("#map, content").removeAttr('style');
            $("#mobile-show-content").show();
            map.invalidateSize(false);
        },

    }
})()




// 
$(window).resize(function () {
    // Code in this block will run when the window
    // is resized to greater than 768px
    if ($(window).width() > RESP_WINDOW_SIZE) {

        // When hiding and showing elements with JQuery, a style tag is inserted into
        // the HTML element itself. The contents of this style tag then overwrite the css,
        // meaning the media queries no longer work. This line resets the "display" so
        // that it falls back to the css, allowing the media queries to work
        $("#sidebar, #map, #resp-map-menu, #resp-sidebar-menu").css('display', '');
        MapUIControl.reset();

    }
// if ($(window).width() <= 768) {
//     $("#map").removeClass("col")
//         .addClass("col-12");
// }



});



function loadSideBarContent(navId){

    if( navId == "routes"){
        routes()
    }

    // Load the appropriate HTML using the navId
    $("#sidebar").load("/" + navId);

    // Set the active navbar item to the one currently displayed
    // for both side nave bar and bottom nav bar
    $(".bottom_nav_item, .nav_item").removeClass("nav-active");
    $("#bottom-" + navId + ", #" + navId).addClass("nav-active");
}

$(document).on("click.mapUI", "#map", MapUIControl.fullscreen)
$(document).on("click.mapUI", "#mobile-show-content", MapUIControl.halfscreen)


