
function routes() {
    // A global variable to hold all the currenly diplayed routed
    var routeLayerObj = {};
    var routeStopsLayer;
    var stopsObj = {};
    // Will hold the route currently being displayed in the side bar
    var currentRoute = undefined;


    // Wait for the document to finish loading
    $(document).ready(function () {
        $(document).off("click.routes")
        addOnclicksToVariations()
        // Add the route filter to the search box
        $('#route-filter').on('keyup search', () => {
            filterRouteList()
        });

        // On click for the back button when route variations are
        // showing
        // Hides the variations div and shows the routes list
        $(document).on("click.routes", "#back-to-routes", function () {
            removeRouteStopsFromMap();
            toggleRouteDisplay(currentRoute)
            MapUIControl.hidemap();
            $("#route-stop-div").fadeOut(10);
            $("#variations-accordion").html("");
            $("#routes-div").fadeIn(10);
            $("#route-stops-title").html("")

        });

        $(document).on("click.routes", "#inbound-radio, #outbound-radio", function () {
            let direction = $(this).attr("data-inbound")

            console.log("radio click" + direction);
            removeRouteStopsFromMap()
            toggleRouteDisplay(currentRoute);
            toggleRouteDisplay(currentRoute, direction);

            // Show a list of the variations 
            showRouteVariations(currentRoute, direction);
        });



        $(document).on("click.routes", '.bottom_nav_item', function () {
            // MapUIControl.reset();
            MapUIControl.hidemap();
            removeRouteStopsFromMap();
            for (const route in routeLayerObj) {
                removeRouteFromMap(route);
            }
        });



        // get all routes from django
        $.getJSON("api/routes/routename", function (data) {

            // Get the routenames from the data
            let routes = [];
            let operators = []
            data.forEach(route => {
                routes.push([route.route_name, route.operator]);
                if (operators.indexOf(route.operator) === -1) {
                    operators.push(route.operator)
                }
            });

            // Sort them nicely
            routes.sort((a, b) => {
                return alphanumSort(a[0], b[0]);
            });
            let opFilter = $("#operator-filter");
            opFilter.html("");

            operators.sort();
            operators.forEach((op, idx) => {
                opFilter.append(`<div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckbox${idx}" value="option${idx}">
                            <label class="form-check-label" for="inlineCheckbox${idx}">${op}</label>
                        </div>`);
            });


            // Add the routes to the list
            // Add the stars to the list
            let content = '';
            routes.forEach(route => {
                content += renderRouteListItem(route[0], route[1]);
            });

            // Display the routes
             $("#routes-list").append(content);


            //  $(".star").click(function () {
            //     $(this).toggleClass("far fa-star fas fa-star");
            //  });


//第一次會catch然後return，第二次如果存在就不save
             $('.star').click(function(e){
                e.preventDefault;
                let starredRoute = $(this).attr("data-route");
                var routesList = [];
                routesList.push(starredRoute);
                try{
                    cookiemonster.get('routesList');
                }catch{
                    cookiemonster.set('routesList', routesList, 3650);
                    alert('Save Sucessfully');
                    return ;
                }

                var previous_route = cookiemonster.get('routesList');
                var flag = 0;

                for(let i=0;i<previous_route.length;i++){
                    if(starredRoute==previous_route[i]){
                        alert('This route is already in the list');
                        flag = 1;
                    }
                }
                    if (flag==0){
                        try{
                            cookiemonster.get('routesList');
                            cookiemonster.append('routesList', routesList, 3650);
                            
                        } catch{
                            cookiemonster.set('routesList', routesList, 3650);
                        }
                        alert('Save Sucessfully');
                    }

                });






            // Add an on click to each route
            $(document).on("click.routes", ".route-item", function () {

                MapUIControl.halfscreen()


                $("#inbound-radio").prop('checked', true)
                    .parent().addClass("active");
                $("#outbound-radio").prop('checked', false)
                    .parent().removeClass("active");

                // Hide the all routes div
                $("#routes-div").fadeOut(10);

                // get the ID of the element clicked
                let routeElemId = $(this).attr('id');

                // Get the route name from the ID
                routeName = routeElemId.split("-")[1];
                $("#route-stops-title").html(routeName)
                $("#route-stop-div").fadeIn(400);

                currentRoute = routeName;
                // Toggle display of the route on the map as needed
                toggleRouteDisplay(routeName)

                // Show inbound routes by default
                let inbound = 1;

                // Show a list of the variations 
                showRouteVariations(routeName, inbound);
            });
        });
    });







    // Show a list of route variations
    // Returns a promise so .then() can be used to execute code
    // when it is done
    function showRouteVariations(routeName, inbound) {
        // Get the variation based on route name and direction
        $("#variations-accordion").html("");
        return $.getJSON("api/routes/variations/",
            { name: routeName, inbound: inbound },
            function (variations) {
                $("#variations-accordion").html("");
                // Display the variations
                let content = '';
                variations.forEach((variation, index) => {
                    content += renderVariationAccordionItem(variation.towards, variation.shape_id, index);
                });
                $("#variations-accordion").append(content);
            });

    }


    function addOnclicksToVariations() {
        $(document).on("click.routes", ".stops-list-button", function () {
            removeRouteStopsFromMap()
            // Each variation in the list has its unique shape id
            // stored in a data-shape-id attribute
            let shapeId = $(this).attr('data-shape-id');
            let index = $(this).attr('data-index');
            // Get a list of stops using the shape id
            $.getJSON("api/routes/stops/", { shape: shapeId }, function (stops) {
                // Sort the stops in the order they appear on the route.
                stops.sort((a, b) => {
                    return a.seq - b.seq;
                });
                // Create a list item for each stop and add it to the list
                console.log(stops)
                let stopMarkers = []
                let content = '';
                stops.forEach(stop => {
                    content += renderStopListItem(stop.stop_name, stop.id, shapeId)
                    let stopMarker = new L.CircleMarker([stop.lat, stop.lon], { radius: 6, fillOpacity: 0.5 });
                    stopMarker.setStyle({
                        color: 'green',
                    });
                    stopMarker.stopId = stop.id;
                    stopMarker.shapeId = shapeId;
                    stopMarker.on("click", displayTimetable)
                        .on("mouseover", highlightStop)
                        .on("mouseout", unHighlightStop)
                        .addTo(map);
                    stopMarkers.push(stopMarker);
                    stopsObj[stop.id] = stopMarker

                });

                routeStopsLayer = L.featureGroup(stopMarkers).addTo(map);
                $(`#stops-list-${index}`).append(content);

                // Add on clicks to the stops
                $(".stop-item").off("click");
                $(".stop-item").click(displayTimetable);

                $(".stop-item").off("hover");
                // .hover takes two functions, one for mouseover and one for mouse away
                // Here we change the styling of the stop on the map for the list item that's
                // hovered over
                $(".stop-item").hover(highlightStop, unHighlightStop);
            });
        });

    }



    function displayTimetable(e) {
        // Get the stop id and stop name from the clicked element
        let stopId = $(this).attr('data-stop-id');
        let shapeId = $(this).attr('data-shape-id');
        console.log(this);
        console.log(stopId);
        if (!stopId) {
            stopId = this.stopId
            shapeId = this.shapeId
        }
        let stopName = $("#stop-" + stopId).html()

        // Set the title of the timetable
        $("#timetable-title").html(stopName);

        // Toggle display of the timetable modal (pop up box)
        // And remove any previous info it contained
        $('#timetable-modal').modal('toggle');

        $("#timetable-tabs, #timetable-content").html("")
            .hide();

        $("#timetable-loader").show();

        // Get the timetable for this route variation at this stop
        return $.getJSON("/api/stoptime/timetable",
            { shape: shapeId, stop_id: stopId },
            function (timetables) {
                // Show the modal content
                $("#timetable-tabs").show();
                $("#timetable-content").show();

                $("#timetable-loader").hide();
                // Populate the modal with the timetable
                fillTimetableModal(stopName, timetables);
            });
    }

    function highlightStop() {
        let stopId = $(this).attr('data-stop-id');
        let allowCentrePan = true;
        if (!stopId) {
            stopId = this.stopId
            allowCentrePan = false;
        }
        let latLng = stopsObj[stopId].getLatLng();
        stopsObj[stopId].setStyle({
            color: 'orange',
            weight: 10,
        })
            .setRadius(10)
            .bringToFront();
        if (allowCentrePan) {
            map.panTo(latLng);
        }
    }

    function unHighlightStop() {
        let stopId = $(this).attr('data-stop-id');
        if (!stopId) {
            stopId = this.stopId
        }
        stopsObj[stopId].setStyle({
            color: 'green',
            weight: 5,
        })
            .setRadius(6);
    }



    // Populate the modal with the timetable
    function fillTimetableModal(stopName, timetables) {

        // chunk size dictates how many times will be displayed in 
        // each row of the timetable
        const CHUNK_SIZE = 6;

        // The time table is a dict with keys like "Mon-Fri"
        // or Sun. These are sorted alphabetically by default
        // so here they are sorted by day of the week
        timetableKeys = Object.keys(timetables);
        timetableKeys.sort(sortByDay);

        // Loop through the keys
        let idx = 0
        timetableKeys.forEach(days => {
            // Create the tab and an empty pane
            let tabAndPane = renderNavTabAndPane(days, idx);
            $("#timetable-tabs").append(tabAndPane.tab);
            $("#timetable-content").append(tabAndPane.pane);

            // Make a list of all the times
            timesArr = []
            timetables[days].forEach(time => {
                timesArr.push(time.time)
            });
            // Sort the times
            timesArr.sort();

            // Convert the time from seconds after midnight to a human readable format
            timesArr = timesArr.map(time => {
                return new Date((time % 86400) * 1000).toISOString().substr(11, 5);
            });

            // Split the times into chunks, one chunk for each row
            timeChunks = chunkArray(timesArr, CHUNK_SIZE);

            // Add the times to the timetables
            timeChunks.forEach(times => {
                let row = renderTimetableRow(times)
                $(`#timetable-table-${idx}`).append(row)
            });

            idx++;
        });

        // Initialise the tooltips
        $('[data-toggle="tooltip"]').tooltip()
    }




    // Function to display a route on the map
    // Direction should be 1 for inbound, 0 for outbound
    // Colour will be used to display the route on the map

    function displayRouteOnMap(routeName, direction, colour) {
        map.invalidateSize(false);
        let routeObj = {};

        // Get the data geojson formate from django 
        return $.getJSON("/api/shapes/geo_json/",
            { routename: routeName, inbound: direction },
            function (routeGeoJson) {

                // Some settings for displaying the line on the map
                var style = {
                    "color": "#CD0000",
                    "weight": 5,
                    "opacity": 0.65
                };


                routeObj = {};
                let routes = []
                routeGeoJson.forEach(route => {
                    routes.push(L.geoJSON(route, {
                        style: style,
                        onEachFeature: eachFeature
                    })
                    );
                });



                let routesLayer = L.featureGroup(routes).addTo(map);

                currentBounds = routesLayer.getBounds();
                map.flyToBounds(currentBounds, { 'duration': 0.8 });

                // routeLayerObj holds all routes currently on the map, allowing them
                // to be easily deleted later
                routeLayerObj[routeName] = routesLayer;
            });




        function eachFeature(feature, layer) {
            // store reference
            let shapeId = feature.properties.shapeId
            routeObj[shapeId] = layer;
            let button = $("#variations-accordion").find(`[data-shape-id='${shapeId}']`);

            // .hover takes two functions, one for mouseover and one for mouse away
            // Here we change the styling of the route on teh map for the button that's
            // hovered over
            button.hover(() => {
                routeObj[shapeId].setStyle({
                    color: 'blue',
                    weight: 10,
                });
                routeObj[shapeId].bringToFront();
            }, () => {
                routeObj[shapeId].setStyle({
                    color: 'red',
                    weight: 5,
                });
            });
        }
        // call from outside map
        function highlightFeature(id) {
            layers[id].setStyle({
                fillOpacity: 0.5
            });
        }

    }



    function removeRouteStopsFromMap() {
        console.log("removing siots");

        if (routeStopsLayer) {
            map.removeLayer(routeStopsLayer);
            routeStopsLayer = undefined;
        }

    }



    // function to remove a route from the map
    function removeRouteFromMap(routeName) {
        // Get map layer from the routeLayerObj and remove it
        map.removeLayer(routeLayerObj[routeName]);

        // delete map layer from routeLayerObj
        delete routeLayerObj[routeName];
    }



    // Function to toggle the display of a route using a route name
    // Also add the background colour to the list item in the sidebar
    function toggleRouteDisplay(routeName, direction = 1) {

        // Get the list element for the route to be toggled
        let routeListElementID = $("#route-" + routeName)

        // Check is the route is being displayed or not
        if (routeLayerObj[routeName]) {

            removeRouteFromMap(routeName);

        } else {

            displayRouteOnMap(routeName, direction, '#FFFFFF')
                .then(() => {

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

    // ========= RENDER FUNCTIONS =========
    // These are all functions for rendering various elements dynamically

    // create and return list-group-item for route
    function renderRouteListItem(route, operator) {
        const content = `
        
            <li class="list-group-item route-item" id="route-${route}">
                <ul>
                    <li class="row">
                    <span class="col-1"><i class='far fa-star star' data-route="${route}"></i></span>
                        <b class="col-6">${route}</b>
                        <span class="col-5">${operator}</span>
                    </li>
                </ul>
            </li>`;
        return content;
    }

    function renderStopListItem(stop, id, shapeId) {
        const content = `
            <li class="list-group-item stop-item" data-stop-id="${id}" data-shape-id="${shapeId}">
                <ul>
                    <li class="row"  id="stop-${id}">${stop}</li>
                </ul>
            </li>`;
        return content;
    }



    function renderVariationAccordionItem(destination, id, index) {
        const content = `
            <div class="card">
                <div class="card-header" id="heading-${index}">
                    <h2 class="mb-0">
                        <button class="btn btn-secondary btn-block stops-list-button" type="button" data-toggle="collapse"
                                data-target="#collapse-${index}"
                                aria-expanded="true"
                                aria-controls="collapse-${index}"
                                data-shape-id="${id}"
                                data-index="${index}">
                            Towards ${destination}
                        </button>
                    </h2>
                </div>

                <div id="collapse-${index}" class="collapse" aria-labelledby="heading-${index}"
                    data-parent="#variations-accordion">
                    <div class="card-body">
                        <ul class="list-group list-group-flush stops-list" id="stops-list-${index}">
                        </ul>
                    </div>
                </div>
            </div>`;
        return content;
    }






    // Render the tab and the pane for displaying the timetables
    function renderNavTabAndPane(days, index) {

        // Active and show determine which tab and pane are currently
        // being displayed. By default the first tab will show
        let active, show;
        if (index == 0) {
            active = "active";
            show = "show";
        } else {
            active = "";
            show = "";
        }
        let tab = ` <a class="nav-item nav-link ${active}" id="nav-tab-${index}" data-toggle="tab" href="#timetable-${index}" role="tab"
                            aria-controls="nav-home" aria-selected="true">${days}</a>`;

        let pane = `<div class="tab-pane fade ${show} ${active}" id="timetable-${index}" role="tabpanel">
                        <table class="table table-sm">
                            <tbody id="timetable-table-${index}"></tbody>
                        </table>
                    </div>`;

        return { tab: tab, pane: pane };
    }


    // Render each row for the timetable
    function renderTimetableRow(times) {
        let content = "<tr>";
        times.forEach(time => {
            content += `<td data-toggle="tooltip" title="Usually 5-10 mins late">${time}</td>`;
        });
        content += "</tr>";
        return content;
    }



    // https://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
    function getTextColour(color) {
        if (color.length == 7) {
            color = color.substring(1);
        }
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


    // Take two days and sort them in order of the week
    // For use in the .sort() method
    function sortByDay(day1, day2) {
        let daysInOrder = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
        day1 = day1.substr(0, 3).toLowerCase();
        day2 = day2.substr(0, 3).toLowerCase();

        day1 = daysInOrder.findIndex(day => day == day1);
        day2 = daysInOrder.findIndex(day => day == day2);
        return day1 - day2;
    }

    //https://ourcodeworld.com/articles/read/278/how-to-split-an-array-into-chunks-of-the-same-size-easily-in-javascript
    function chunkArray(myArray, chunk_size) {
        var results = [];

        while (myArray.length) {
            results.push(myArray.splice(0, chunk_size));
        }

        return results;
    }

}


// function toggleMobileMap() {
//     $(".sidebar_header").hide();
//     $("#map").show()
//         .height(0)
//         .animate({ height: "200px" }, 500, () => map.invalidateSize(false));

// }

// function fullscreenMobileMap() {
//     $(".sidebar_header").hide();
//     $("#map").show()
//         .animate({ height: "500px" }, 500, () => map.invalidateSize(false));
// }




