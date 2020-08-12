function stops() {
    currentBounds = undefined;
    currentCentre = [53.346967, -6.259923];
    MapUIControl.halfscreen();
    $(document).off("click.stops")

    //event will be called when map bounds change
    // This is put in a function so the moveend can be removed when not on the stops tab
    map.on('moveend', displayStops);

    function displayStops() {
        // This if is checking if the map is resizing on mobile
        // But it doens't seem to work at the moment
        if (MapUIControl.allowStopReload) {
            var mapCentra = map.getCenter();
            //update centreLocation to centre of the map
            centreLocation = [mapCentra["lat"], mapCentra["lng"]];

            //clear all the markers in the layer
            stopsLayer.clearLayers();
            //clear all the elements in list group
            showStops(centreLocation[0], centreLocation[1]);
            updateStopFavourites();
        } else {
            console.log("Blocked===")
        }
    }

    $(document).ready(function () {
        $("#stop-realtime-div").fadeOut(10);
        $("#stops-div").fadeIn(10);

        //clear all the markers in the layer
        stopsLayer.clearLayers();

        var mapCentra = map.getCenter();
        //update centreLocation to centre of the map
        centreLocation = [mapCentra["lat"], mapCentra["lng"]];

        showStops(centreLocation[0], centreLocation[1]);
        initAutoComplete();
        updateStopFavourites();
    });


    $(document).on("click.stops", '.nav_item, .bottom_nav_item', function () {
        stopsLayer.clearLayers();
        map.off('moveend', displayStops);
    });


    // Shows Stops and distances 
    function showStops(lat, lng) {
        $("#stop-loader").show();
        $("#stopsListGroup").html("");
        $("#no-stops-warning").hide();
        $.getJSON(`/api/stops/nearby?latitude=${lat}&longitude=${lng}&radius=1`, function (data) {
            content = '';
            $.each(data, function (i, stop) {
                // content += document.getElementById('routes-list').innerHTML = "<a href='#'><i class='far fa-star star'></a>"
                // Get distance from centre location to every stop in kilometers
                dist_kms = distance(lat, lng, stop.latitude, stop.longitude, 'K');
                dist_ms = Math.round(dist_kms * 1000);
                content += renderStopListItem(stop, dist_ms);
                markStopsOnMap(stop);
            });
            $("#stop-loader").hide();
            $("#stopsListGroup").html(content);

            let visible = $(content).length;
            if (visible == 0) {
                $("#no-stops-warning").show();
            } else {
                $("#no-stops-warning").hide();
            }
        });
    }




    function moveMapToEnteredAddress(address) {
        $.getJSON(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=AIzaSyBavSlO4XStz2_RD_fUBGwm89mQwGwYUzA`, function (data) {
            var latlng = data.results[0].geometry.location;
            //map.panTo(new L.LatLng(latlng.lat, latlng.lng))
            showStops(latlng.lat, latlng.lng);
            map.flyTo([latlng.lat, latlng.lng], 15, {
                animate: true,
                duration: 1.5
            });
        });
    }



    $('form').submit(function (e) {
        // Stop form refreshing page on submit
        e.preventDefault();
        //get value entered by users
        var area = document.forms["stops-area"]["stops_area"].value
        //pass value to the address finding function
        moveMapToEnteredAddress(area);
    });


    function showArrivingBusesOnSideBar(stopid) {
        //get realtime data
        $("#realtime-loader").show();
        $("#no-realtime-warning").hide();
        
        $.getJSON(`/realtimeInfo/${stopid}`, function (data) {
            // parse response data to json 
            obj = JSON.parse(data)
            if (obj.errorcode == "0") {
                results = obj.results;
                content = '';
                $.each(results, function (i, bus) {
                    content += renderRealtimeListItem(bus);
                });
                $("#realtime-loader").hide();
                $("#stopRealtimeListGroup").html(content);
            } else {
                $("#realtime-loader").hide();
                $("#no-realtime-warning").show();
            }
        });
    }

    // $(document).on("click", ".star2", function() {

    //     //get the stop attribute associate with the selected star and push to a list
    //     let starredStop = $(this).attr("data-stop");
    //     var stopsList = [];
    //     stopsList.push(starredStop);

    //         //if the stop is not in the list it will be saved in cookies
    //     // try{
    //     //     cookiemonster.get('stopsList');
    //     // }catch{
    //     //     cookiemonster.set('stopsList', stopsList, 3650);
    //     //     return ;
    //     // }

    //     var previous_stops = cookiemonster.get('stopsList');
    //     var flag = 0;

    //     //if selected stop already in the list wont save again
    //     for(let i=0;i<previous_stops.length;i++){
    //         if(starredStop==previous_stops[i]){
    //             alert('This stop is already in the list');
    //             flag = 1;
    //         }
    //     }

    //     //if it is not in the list then will append to cookies 
    //         if (flag==0){
    //             try{
    //                 cookiemonster.get('stopsList');
    //                 cookiemonster.append('stopsList', stopsList, 3650);

    //             } catch{
    //                 cookiemonster.set('stopsList', stopsList, 3650);
    //             }
    //             alert('Save Sucessfully');
    //         }
    // });

    // create and return list-group-item for stop
    // stop_dist added as item
    function renderStopListItem(stop, stop_dist, fav = false) {
        //function now recieves stopid instead so need to get stop info
        // need to do some jiggery pokery to the stop-routes to return the info without brackets or quotations
        var route_list = stop.routes;
        route_list = route_list.slice(2, -2);
        route_list = route_list.split("', '");
        // Getting routes to display as buttons for style purposes
        route_buttons = '';
        for (var i = 0; i < route_list.length; i++) {
            route_buttons += '<button type="button" class="btn btn-outline-secondary" id="stop-button">' + route_list[i] + "</button>";
        }

        let favStr = "";
        let solid = "far";
        if (fav) {
            favStr = "fav-";
            solid = "fas"
        }

        const content = `


      <li class="list-group-item stop" id="station-${stop.stopid}">
          <ul class="row pl-0">
                <span class="col-1">
                    <a href="#">
                        <i id="${favStr}star-stop-${stop.stopid}"class="${solid} far fa-star star2 stop-star" data-stop="${stop.stopid}"></i>
                    </a>
                </span>
              <li class="col-8"><b>${ stop.fullname},</b> Stop ${stop.stopid}</li>
              <li class="col-3">${ stop_dist} Metres</li>
              <div class="row"><div class="col-12 pl-5 pt-3"> ${ route_buttons}</div></div>
          </ul>
      </li>`;

        return content;
    }



    function renderRealtimeListItem(bus) {

        const content = `
          <li class="list-group-item stop-realtime" id="route-${bus.route}">
              <ul class="row">
                  <li class="col-2"><b>${ bus.route}</b></li>
                  <li class="col-6">${ bus.destination}</li>
                  <li class="col-4">${ bus.duetime} mins </li>
              </ul>
          </li> `;
        return content;
    }

    $(document).on("click.stops", "#back-to-stops", function () {

        $("#stop-realtime-div").fadeOut(10);
        $("#stops-div").fadeIn(10);
    });


    function markStopsOnMap(stop) {
        // fixing the printing of array issue on marker
        var route_list = stop.routes;
        route_list = route_list.slice(2, -2);
        route_list = route_list.split("', '");

        route_buttons = ''
        for (var i = 0; i < route_list.length; i++) {
            route_buttons += `<button type="button" class="btn btn-outline-secondary" style="font-size: 10pt; padding: 2px; margin: 1px;">` + route_list[i] + "</button>";
        }

        var marker =
            L.marker([stop.latitude, stop.longitude])
                .bindPopup(`<b> ${stop.localname}</b><br> ${route_buttons}`);
        stopsLayer.addLayer(marker);
    }


    //Click function for bus stop list-item
    $('.list-group-flush').on('click.stops', '.stop', function (e) {
        // Get the name of tab on the navbar that was clicked

        $("#stopRealtimeListGroup").html("")
        var id = $(this).attr('id').replace("station-", "");;
        showArrivingBusesOnSideBar(id);

        $("#stop-realtime-div").fadeIn(10);
        $("#stops-div").fadeOut(10);
    });



    // Function to calculate the distance between two points
    function distance(lat1, lon1, lat2, lon2, unit) {
        if ((lat1 == lat2) && (lon1 == lon2)) {
            return 0;
        }
        else {
            var radlat1 = Math.PI * lat1 / 180;
            var radlat2 = Math.PI * lat2 / 180;
            var theta = lon1 - lon2;
            var radtheta = Math.PI * theta / 180;
            var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
            if (dist > 1) {
                dist = 1;
            }
            dist = Math.acos(dist);
            dist = dist * 180 / Math.PI;
            dist = dist * 60 * 1.1515;
            if (unit == "K") { dist = dist * 1.609344 }
            if (unit == "N") { dist = dist * 0.8684 }
            return dist;
        }
    }

    function initAutoComplete() {

        //add restriction for autocomplete places API
        var options = {
            componentRestrictions: { country: "IE" }
        };

        function initAutocomplete(input) {
            //use Google Place Autocomplete for input box
            //source: https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
            var autocomplete = new google.maps.places.Autocomplete(input, options);

            // Set the data fields to return when the user selects a place.
            autocomplete.setFields(
                ['address_components', 'geometry', 'icon', 'name']);

            autocomplete.addListener('place_changed', function () {
                var place = autocomplete.getPlace();
                if (!place.geometry) {
                    // User entered the name of a Place that was not suggested and
                    // pressed the Enter key, or the Place Details request failed.
                    window.alert("No details available for input: '" + place.name + "'");
                    return;
                }

                var address = '';
                if (place.address_components) {
                    address = [
                        (place.address_components[0] && place.address_components[0].short_name || ''),
                        (place.address_components[1] && place.address_components[1].short_name || ''),
                        (place.address_components[2] && place.address_components[2].short_name || '')
                    ].join(' ');
                }
            });
        }

        initAutocomplete(stops_area);
    }

    $("#stopsListGroup, #fav-stops-list").on("click.stops", '.star2', function (e) {
        console.log(e)
        e.stopPropagation();
        // Get the clikced stop
        const starredStopID = $(this).attr("data-stop");
        let stopinfo;
        $("#fav-stops-div").show();
        $("#stop-favs-loader").show();
        $("#fav-stops-list").html("");
        $.getJSON(`/api/stops/${starredStopID}`, function (data) {
            stopinfo = JSON.stringify(data);
            console.log("This is the (hopefully stringified) data: ", stopinfo);

            let currentStopsList;

            try {
                // Check if the stopList cookie exists
                // If so, get the list
                currentStopsList = cookiemonster.get('stopsList');
            } catch{
                // If not just add the clicked stop to the list and return
                console.log("Setting cookie to ", [stopinfo])
                cookiemonster.set('stopsList', [stopinfo], 3650);
                updateStopFavourites()
                return;
            }


            // Check if the clicked stop is in the cookies array
            const index = currentStopsList.indexOf(stopinfo);
            if (index > -1) {
                console.log("made it in")
                // if index > -1 the stop is alreay in the cookies,
                // we can remove it from the array
                console.log("stopinfo pre slice", stopinfo)

                currentStopsList.splice(index, 1);
                console.log('index: ', index);
                console.log("stopinfo post slice", stopinfo);
            } else {
                // Otherwise we add to the array
                currentStopsList.push(stopinfo);
            }

            // Set the cookies  with the new list
            cookiemonster.set('stopsList', currentStopsList, 3650);



            // Update the favourites display
            updateStopFavourites();
        });
    });


    function updateStopFavourites() {
        $(".stop-star").removeClass("fas");
        $(".stop-star").addClass("far");
        
        let stopsList;
        try {
            stopsList = cookiemonster.get('stopsList');
        } catch{
            $("#fav-stops-div").hide();
            return;
        }

        if (stopsList.length == 0) {
            $("#fav-stops-div").hide();
            console.log('fav stops hide 2');
            return;
        }

        $("#fav-stops-list").html("");
        stopsList.forEach(stop => {
            stop = JSON.parse(stop)
            $("#star-stop-" + stop.stopid).removeClass("far")
                .addClass("fas");
            //Get stop info required for render stopListitem
            var lat = centreLocation[0];
            var lng = centreLocation[1];
            var dist_kms = distance(lat, lng, stop.latitude, stop.longitude, 'K');
            var dist_ms = Math.round(dist_kms * 1000);
            let content = renderStopListItem(stop, dist_ms, fav = true);
            $("#fav-star-stop-" + stop.stopid).removeClass("far")
                .addClass("fas");
            $("#fav-stops-list").append(content);
            $("#fav-stops-div").show();
            $("#stop-favs-loader").hide();
        });
    }


}