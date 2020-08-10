const RESP_WINDOW_SIZE = 768;
const MAP_ZOOM_NUM = 12;
let currentBounds;
let currentCentre;
let allowStopReload = true;
let DateTime = luxon.DateTime;
let dublinCoords = [53.3373266,-6.2752625]
// Code in this block will be run one the page is loaded in the browser
$(document).ready(function () {


    // on click function for nav-items
    $('.nav_item').click(function () {

        // Get the name of tab on the navbar that was clicked
        var nav_id = $(this).attr('id');

        // log nav btn click event to firebase 
        analytics.logEvent('select_content', { content_type: 'navi_item', item_id: nav_id });

        // Update sidebar content with appropriate html
        loadSideBarContent(nav_id);
    });

    // on click function for bottom-nav-items
    // This is slightly different to the side-bar nav
    // as it also shows and hides the map
    $('.bottom_nav_item').click(function () {
        // Get the name of tab on the navbar that was clicked
        MapUIControl.hidemap();
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
    // Load the journey UI content by default
    loadSideBarContent("journey");

});



//centreLocation: default value is Dublin city centre,
//If user allow location access, than set value to user location
var centreLocation = [53.3482, -6.2641]
L.control.attribution(false);
// Initialize and add the map
var map = L.map('map', { attributionControl: false }).setView(centreLocation, MAP_ZOOM_NUM);

//init layers for storeing all stop, journey, userlocation markers
var stopsLayer = L.layerGroup().addTo(map);
var journeyLayer = L.layerGroup().addTo(map);
var userLocationLayer = L.layerGroup().addTo(map);

function clearElementsInLayers() {
    //clear all the markers in the layer
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();
}



function initMap() {
    
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: MAP_ZOOM_NUM,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoib2hteWhhcHB5IiwiYSI6ImNrYjdyaWg0cDA0bXMycXFyNzgxdmkyN3kifQ.gcq3O8-AveWKXNS5TUGL_g'
    }).addTo(map);

    map.locate({ setView: true, watch: true });

    // if geolocation is available
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            
            // create custom icon
            var customIcon = L.icon({
                iconUrl: './static/img/user_marker.png',
                iconSize: [35, 45], // size of the icon
            });
                
            var marker = L.marker([position.coords.latitude, position.coords.longitude], {icon: customIcon})
            .addTo(map)
            .bindPopup("Centre");
            
            userLocationLayer.addLayer(marker);
            centreLocation = [position.coords.latitude, position.coords.longitude];
            currentCentre = centreLocation;
            map.setView(centreLocation, MAP_ZOOM_NUM);
        });
    } 
    

    // on click function for my location btn
    $('#my_location_btn').click(function () {
        map.setView(centreLocation, MAP_ZOOM_NUM);
    });
}


var MapUIControl = (function () {

    return {
        isFirstTime: true,
        isHidemap: true,
        isHalfscreen: false,
        isFullscreen: false,
        hidemap: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                this.isHalfscreen = false;
                this.isHidemap = true;
                this.isFullscreen = false;
                $('#sidebar').fadeIn(200);
                $(".sidebar-header").fadeIn(200);
                $("#map").animate({ height: "0px" }, 500, () => {
                    // $("#map").hide();
                    $("#mobile-show-content").hide();
                });
            }
        },

        halfscreen: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                this.isHalfscreen =true;
                this.isHidemap=false;
                this.isFullscreen=false;
                allowStopReload = false;
                $(".sidebar_header").hide();
                $("#mobile-show-content").hide();
                $('#sidebar').fadeIn(10);
                // $("#map").show()
                $("#map").animate({ height: "200px" }, 500, () => {

                    console.log("Invalidating size")
                    map.invalidateSize(false);
                    if(this.isFirstTime){
                        map.flyTo(dublinCoords, 12, { 'duration': 0.5 });
                        this.isFirstTime = false;
                    }
                    allowStopReload = true;
                    if (currentBounds) {
                        console.log("flyint to bounds");
                        console.log(currentBounds);
                        map.flyToBounds(currentBounds, { 'duration': 0.5 });
                    } else if (currentCentre) {
                        // console.log("flyint to centre");
                        // console.log(currentCentre);
                        // map.flyTo(currentCentre, 12, { 'duration': 0.5 });
                    }
                });
            }
        },

        fullscreen: function () {
            if ($(window).width() < RESP_WINDOW_SIZE) {
                this.isHalfscreen = false;
                this.isHidemap = false;
                this.isFullscreen = true;
                allowStopReload = false;
                $(".sidebar_header").hide();

                var newHeight = $(window).height() - 80 - 60 - 50 + 5;
                $('#sidebar').fadeOut(10);
                $("#mobile-show-content").show();
                // $("#map").show()
                $("#map").animate({ height: newHeight }, 500, () => {
                    map.invalidateSize(false);
                    allowStopReload = true;
                    if (currentBounds) {
                        map.flyToBounds(currentBounds, { 'duration': 0.5 });
                    } else if (currentCentre) {
                        // map.flyTo(currentCentre, 12, { 'duration': 0.5 })
                    }
                });
            }
        },
        reset: function () {
            $("#map, content").removeAttr('style');
            $("#mobile-show-content").hide();
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


});



function loadSideBarContent(navId) {
    console.log("loadgin...")
    console.log(navId)

    // Load the appropriate HTML using the navId
    $("#sidebar").load("/" + navId, () => {
        switch (navId) {
            case "routes":
                routes();
                break;
            case "journey":
                journey();
                break;
            case "stops":
                stops();
                break;
            default:
                break;
        }
    });
    // Set the active navbar item to the one currently displayed
    // for both side nave bar and bottom nav bar
    $(".bottom_nav_item, .nav_item").removeClass("nav-active");
    $("#bottom-" + navId + ", #" + navId).addClass("nav-active");
}


$(document).on("click.mapUI", "#map", MapUIControl.fullscreen)
$(document).on("click.mapUI", "#mobile-show-content", MapUIControl.halfscreen)




