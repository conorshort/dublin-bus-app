
// A global variable to hold all the currenly diplayed routed
// ====== TODO: currently the routes break when the user navigates to a different part of the sidebar
// This will need fixing. Likely routeLayerObj will need to be moved to home.js as currnetly it will
// be overwritten everytime Route menu button is pressed
var routeLayerObj = {}

// Wait for the document to finish loading
$(document).ready(function () {


    // Add the route filter to the search box
    $("#route-filter").keyup(function () {
        filterRouteList()
    })


    // get the route from django
    $.getJSON("api/routes/routename", function (data) {

        // Get the routenames from the data
        let routes = [];
        data.forEach(route => {
            routes.push(route.route_name);
        });

        // Sort them nicely
        routes.sort(alphanumSort);

        // Add the routes to the list
        let content = '';
        routes.forEach(route => {
            content += renderListItem(route);
        });

        // Display the routes
        $("#routes-list").append(content);

        // Add an on click that will display the 
        // route on the map
        $(".route-item").click(function () {

            // get the ID of the element clicked
            let routeElemId = $(this).attr('id');

            // Get the route name from the ID
            routeName = routeElemId.split("-")[1];

            // Toggle display of the route as needed
            toggleRouteDisplay(routeName)
        });
    });
})


// create and return list-group-item for route
function renderListItem(route) {
    const content = `
    <li class="list-group-item route-item" id="route-${route}">
        <ul>
            <li class="row"><b>${route}</b> <span class="route-loading-span"></span></li>
        </ul>
    </li>`;
    return content;
}



// Function to display a route on the map
// Direction should be 1 for inbound, 0 for outbound
// Colour will be used to display the route on the map
function displayRouteOnMap(routeName, direction, colour) {

    // Get the data geojson formate from django 
    return $.getJSON("/api/shapes/geo_json/",
        { routename: routeName, inbound: direction },
        function (routeGeoJson) {

            // Some settings for displaying the line on the map
            var style = {
                "color": colour,
                "weight": 5,
                "opacity": 0.65
            };

            // Add the route geojson to the map
            let routeLayer = L.geoJSON(routeGeoJson, {
                style: style,
            }).addTo(mymap);

            // routeLayerObj holds all routes currently on the map, allowing them
            // to be easily deleted later
            routeLayerObj[routeName] = routeLayer
        });
}


// function to remove a route from the map
function removeRouteFromMap(routeName) {
    // Get map layer from the routeLayerObj and remove it
    mymap.removeLayer(routeLayerObj[routeName]);

    // delete map layer from routeLayerObj
    delete routeLayerObj[routeName];
}



// Function to toggle the display of a route using a route name
// Also add the background colour to the list item in the sidebar
function toggleRouteDisplay(routeName) {

    // Get the list element for the route to be toggled
    let routeListElementID = $("#route-" + routeName)

    // Check is the route is being displayed or not
    if (routeListElementID.hasClass("route-active")) {

        // If it is make it no longer active
        routeListElementID.removeClass("route-active")
            .css('background-color', "")
            .css('color', "");

        // Remove it from the map
        removeRouteFromMap(routeName);

    } else {

        // Otherwise add the route

        // Loading spinner
        let span = routeListElementID.find('span');
        span.html('<div class="loader"></div>');

        // Grey out the list elem when loading
        // Also disables click events to stop multiple
        // clicks
        routeListElementID.addClass("route-loading");

        // Generate a random colour
        let colour = '#' + Math.floor(Math.random() * 16777215).toString(16)

        // Decide whether to display black or white text based on the background colour
        let textColour = getTextColour(colour)

        // Displays the route
        // .then will wait for the displayRouteOnMap function to finish
        // before running the function inside it
        displayRouteOnMap(routeName, 1, colour)
            .then( () => {
                //Remove the loading spinner
                span.html("");
                // Set the list element as active and set the colours
                routeListElementID.removeClass("route-loading")
                    .addClass("route-active")
                    .css('background-color', colour)
                    .css('color', textColour);
            });
    }
}





// This function is added to the search box and is called when a key
// is released. It filters the routes in the route list based on the
// input
// adapted from https://www.w3schools.com/howto/howto_js_filter_lists.asp
// ======= TODO: add some text when no routes match =======
function filterRouteList() {

    // Declare variables
    let input, filter, li, b, i, txtValue;
    input = $('#route-filter');

    filter = input.val().toUpperCase();
    li = $('.route-item');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {

        b = li[i].getElementsByTagName("b")[0];
        txtValue = b.textContent || b.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            routeFound = true;
        } else {
            li[i].style.display = "none";
        }
    }
}



// https://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
function getTextColour(color) {
    if (color.length == 7) { color = color.substring(1); }
    var R = parseInt(color.substring(0, 2), 16);
    var G = parseInt(color.substring(2, 4), 16);
    var B = parseInt(color.substring(4, 6), 16);
    percievedBrightness = Math.sqrt(R * R * .241 + G * G * .691 + B * B * .068);
    return percievedBrightness < 130 ? '#FFFFFF' : '#000000';
}



// Function for naturalsort from:
// http://web.archive.org/web/20130826203933/http://my.opera.com/GreyWyvern/blog/show.dml/1671288
// Sorts the route names in a nicer way
function alphanumSort(a, b) {
    function chunkify(t) {
        var tz = [], x = 0, y = -1, n = 0, i, j;

        while (i = (j = t.charAt(x++)).charCodeAt(0)) {
            var m = (i == 46 || (i >= 48 && i <= 57));
            if (m !== n) {
                tz[++y] = "";
                n = m;
            }
            tz[y] += j;
        }
        return tz;
    }

    var aa = chunkify(a);
    var bb = chunkify(b);

    for (x = 0; aa[x] && bb[x]; x++) {
        if (aa[x] !== bb[x]) {
            var c = Number(aa[x]), d = Number(bb[x]);
            if (c == aa[x] && d == bb[x]) {
                return c - d;
            } else return (aa[x] > bb[x]) ? 1 : -1;
        }
    }
    return aa.length - bb.length;
}