var favorite_journey_list = [];

function journey() {
    // shorter method for the document ready event
    $(function () {

        //load script widgets.js before twttr.widgets.load()
        $.getScript("https://platform.twitter.com/widgets.js")
            .done(function () {
                twttr.widgets.load();
            });

        showSearchJourneyDiv(0);
        clearMapLayers();
        initAutoComplete();
        updateFavoriteList();

        let today = new Date();
        let year = today.getFullYear()
        let month = today.getMonth() + 1
        let day = today.getDate()
        let hour = today.getHours();
        let min = today.getMinutes();

        //init datetime picker
        $(".datetimeInput").flatpickr({
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: 'today',
            defaultDate: `${year}-${month}-${day} ${hour}:${min}`
        });

        $("#journey-loader").hide();
    });


    function updateFavoriteList() {

        // clear all favorite journey list group
        $("#favorite-journey-list-group").empty();
        try {
            favorite_journey_list = cookiemonster.get('journeyList');
        } catch (error) {
            console.log('cookiemonster get journeyList error:' + error)
        }

        if (favorite_journey_list) {
            favorite_journey_list.forEach(function (element, index) {

                var favorite_journey = JSON.parse(element);
                var origin_name = ((favorite_journey || {}).origin || {}).name,
                    destination_name = ((favorite_journey || {}).destination || {}).name;

                if (origin_name && destination_name) {
                    // render favorite journey list-group-item
                    $("#favorite-journey-list-group").append(
                        `<li class="list-group-item favorite-journey-list-item"> \
                <div class="row"> \
                <div class="col-1 solid-star" id="solid-star-${index}"><i class="fas fa-star starSolid"></i></div> \
                <div class="col-11 favorite-journey-content" id="favorite-journey-content-${index}">
                <b>origin:</b> ${origin_name} </br> \
                <b>destination:</b> ${destination_name}</div></div></li>`);
                }
            });
        }


        // click the favorite journey will fill the origin 
        $('.favorite-journey-content').click(function (e) {
            var id = $(this).attr('id');
            var index = id.replace("favorite-journey-content-", "");
            var favorite_journey = JSON.parse(favorite_journey_list[index]);
            var origin = (favorite_journey || {}).origin,
                destination = (favorite_journey || {}).destination;

            if (origin && destination) {
                updateSearchInput(origin, destination);
            }
        });


        // click the solid star icon on favorite journey 
        // will remove the journey from the cookie journeyList 
        $('.solid-star').click(function (e) {
            var id = $(this).attr('id');
            var index = id.replace("solid-star-", "");
            cookiemonster.splice('journeyList', index, 1, 3650);
            updateFavoriteList();
        });
    }


    function updateSearchInput(origin, destination) {
        var origin_name = (origin || {}).name,
            destination_name = (destination || {}).name,
            origin_coord = (origin || {}).coord,
            destination_coord = (destination || {}).coord;

        if (origin_name && destination_name && origin_coord && destination_coord) {
            $("#f-from-stop").val(origin_name);
            $("#f-to-stop").val(destination_name);
            $("#f-from-stop").attr('coord-data', JSON.stringify(origin_coord));
            $("#f-to-stop").attr('coord-data', JSON.stringify(destination_coord));
        }
        $('#favoriteJourneyModalCenter').modal('toggle');
    }


    function initAutoComplete() {

        //add restriction for autocomplete places API
        var options = {
            componentRestrictions: { country: "IE" }
        };

        var from_input = document.forms["journeyForm"]["f-from-stop"];
        var to_input = document.forms["journeyForm"]["f-to-stop"];

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

                //TODO: not the good way to store coordinate, fund a way to replace this
                //save place coordinate to element id
                input.setAttribute('coord-data', `{"lat":${place.geometry.location.lat()}, "lng":${place.geometry.location.lng()}}`);

                if (place.address_components) {
                    address = [
                        (place.address_components[0] && place.address_components[0].short_name || ''),
                        (place.address_components[1] && place.address_components[1].short_name || ''),
                        (place.address_components[2] && place.address_components[2].short_name || '')
                    ].join(' ');
                }
            });
        }
        initAutocomplete(from_input);
        initAutocomplete(to_input);
    }


    $("#use-user-location").click(function (e) {
        // if geolocation is available
        console.log("setting location");
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function () { }, function () { }, {});
            navigator.geolocation.getCurrentPosition(function (position) {
                console.log("hellooo");
                $("#f-from-stop").val('Your Current Location');
                $("#f-from-stop").attr('coord-data', `{"lat":${position.coords.latitude}, "lng":${position.coords.longitude}}`);
                map.setView([position.coords.latitude, position.coords.longitude], MAP_ZOOM_NUM);
            });
        } else {
            alert('Geolocation is not available. Please accept the location permission.')
        }
    });



    // submit button click event 
    $('form').submit(function (e) {

        //show loader when click submit btn
        $("#journey-loader").show();

        // Stop form refreshing page on submit
        e.preventDefault();

        var originCoord = JSON.parse($('#f-from-stop').attr('coord-data'));
        var destinationCoord = JSON.parse($('#f-to-stop').attr('coord-data'));
        var dateTime = document.forms["journeyForm"]["datetime"].value;
        console.log("dateTime")
        console.log(dateTime)

        // 2020-08-06 14:35
        splitDateTime = dateTime.split(/-| |:/)
        console.log(splitDateTime)
        dt = DateTime.fromObject({
            year: splitDateTime[0],
            month: splitDateTime[1],
            day: splitDateTime[2],
            hour: splitDateTime[3],
            minute: splitDateTime[4],
            zone: 'Europe/London',
        });

        var unix = dt.toSeconds();


        // //get direction from api /api/direction
        $.getJSON(`api/direction?origin=${parseFloat(originCoord.lat).toFixed(7)},${parseFloat(originCoord.lng).toFixed(7)}&destination=${parseFloat(destinationCoord.lat).toFixed(7)},${parseFloat(destinationCoord.lng).toFixed(7)}&departureUnix=${unix}`
            , function (data) {

                var status = (data || {}).status,
                    leg = (data || {}).leg,
                    steps = (leg || {}).steps;

                if (status == "OK" && leg && steps) {

                    var arrival_time_text = ((leg || {}).arrival_time || {}).text,
                        departure_time_text = ((leg || {}).departure_time || {}).text,
                        duration_text = ((leg || {}).duration || {}).text,
                        start_address = (leg || {}).start_address,
                        end_address = (leg || {}).end_address,
                        start_location = (leg || {}).start_location,
                        end_location = (leg || {}).end_location;

                    if (arrival_time_text
                        && departure_time_text
                        && duration_text
                        && start_address
                        && end_address
                        && start_location
                        && end_location) {

                        var transferCount = (JSON.stringify(data).match(/TRANSIT/g) || []).length;
                        displaySearchInfoOnHeader($('#f-from-stop')[0], $('#f-to-stop')[0], $("#datetimePicker")[0]);
                        displayTripSummary(duration_text, transferCount, departure_time_text, arrival_time_text);

                        //render and append origin waypoint
                        var origin_waypoint = renderTransitStop(departure_time_text, start_address, start_location);
                        $("#journey-result-steps").append(origin_waypoint);
                        displayJourneySteps(steps);

                        //render and append origin waypoint
                        var destination_waypoint = renderTransitStop(arrival_time_text, end_address, end_location);
                        $("#journey-result-steps").append(destination_waypoint);

                        //drop origin marker
                        dropMarkerOnMap(start_location.lat, start_location.lng, start_address, "");
                        //drop destinaiton marker
                        dropMarkerOnMap(end_location.lat, end_location.lng, end_address, "");

                        showResultJourneyDiv(10);
                    }
                    MapUIControl.halfscreen();

                } else {
                    alert("No journey planning result, please try input other locations.");
                }

                //hide loader
                $("#journey-loader").hide();
            });
    });


    //save the selected journey to favourite
    $('#hollow-star').click(function (e) {

        $("#hollow-star").hide();

        var fromInput = document.forms["journeyForm"]["f-from-stop"];
        var toInput = document.forms["journeyForm"]["f-to-stop"];
        var originCoord = JSON.parse(fromInput.getAttribute('coord-data'));
        var destinationCoord = JSON.parse(toInput.getAttribute('coord-data'));

        //push all of them into a list then push every new selected journey into a journey list
        var perJourney = JSON.stringify({ "origin": { "name": fromInput.value, "coord": originCoord }, "destination": { "name": toInput.value, "coord": destinationCoord } });

        var journeyList = [];
        journeyList.push(perJourney);

        //if the journey is not in the list it will be saved in cookies
        try {
            cookiemonster.get('journeyList');
        } catch{
            cookiemonster.set('journeyList', journeyList, 3650);
            alert('Save Sucessfully');
            return;
        }

        var previous_journey = cookiemonster.get('journeyList');

        if (previous_journey.includes(perJourney)) {
            alert('This journey is already in the list');
        } else {
            try {
                cookiemonster.get('journeyList');
                cookiemonster.append('journeyList', journeyList, 3650);

            } catch{
                cookiemonster.set('journeyList', journeyList, 3650);
            }
            alert('Save as favorite journey sucessfully');
        }
    });



    $('#edit-journey-input').click(function () {
        showSearchJourneyDiv(10);
        clearSearchResult(10);

    });


    function displaySearchInfoOnHeader(originInput, destinationInput, dateTime) {
        // dictionary to store all the elements which are going to display on frontend
        // key: the element id or class name
        // value: content to append to the element 
        $("#journey-result-from").html(originInput.value)
        $("#journey-result-to").html(destinationInput.value)
        $("#journey-result-datetime").html(dateTime.value)

        var perJourney = JSON.stringify({ "origin": { "name": originInput.value, "coord": JSON.parse(originInput.getAttribute('coord-data')) }, "destination": { "name": destinationInput.value, "coord": JSON.parse(destinationInput.getAttribute('coord-data')) } });
        var index = jQuery.inArray(perJourney, favorite_journey_list);

        if (index > -1) {
            $("#hollow-star").hide();
        } else {
            $("#hollow-star").show();
        }
    }


    function displayTripSummary(duration, transferCount, departure_time, arrive_time) {
        // dictionary to store all the elements which are going to display on frontend
        // key: the element id or class name
        // value: content to append to the element 
        // render duration and count of transfer 
        var duration_tranfer_count = renderContent({
            "Total duration:": "<b>" + duration + "</b>"
                + "&nbsp;&nbsp;&nbsp;&nbsp;"
                + "<b>" + transferCount + "</b>"
                + "  transfers"
        });

        $("#journey-result-detail").html(duration_tranfer_count);
        $("#section-trip-summary").html(departure_time + " &nbsp;&nbsp; <b style='font-size: 30px;'> &#8250; </b>  &nbsp;&nbsp;" + arrive_time);
    }



    function renderTransitStop(timeline, name, coordinates) {
        content = '<div class="transit-stop row" style="margin:0px; padding:0px;"> ';
        content += `<div class="transit-timeline col-3" style="text-align:right; ">${timeline}</div>`
        content += '<div class="col-1" style="margin:0px; padding:0px;"><div style="background: red; border-radius: 50%; width: 24px; height: 24px; margin-left: -3px;"></div></div>';
        content += `<div class="transit-stop-name col-8" style="margin:0px; padding:0px;"><b>${name}</b></div>`;
        content += '</div>'

        return content;
    }



    function renderTransitDetail(step, index) {

        var travel_mode = (step || {}).travel_mode,
            duration_text = ((step || {}).duration || {}).text,
            distance_text = ((step || {}).distance || {}).text;

        content = '<div class="transit-stop row"> ';

        if (travel_mode) {
            if (travel_mode == "TRANSIT") {
                content += `<div class="transit-timeline col-3" style="text-align:right;"><img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon"></div>`
                content += '<div class="col-1"><div style="border-left: 4px solid red; height: 100%;position: absolute;left: 50%; margin-left: -2px; top: 0;"></div></div>';

            } else {
                content += `<div class="transit-timeline col-3" style="text-align:right";><img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon"></div>`
                content += '<div class="col-1"><div style="border-left: 4px dotted red; height: 100%;position: absolute;left: 50%; margin-left: -2px; top: 0;"></div></div>';
            }

            content += '<div class="transit-detail col-8" style="padding-top: 20px; padding-bottom: 20px;">';
            content += `<div class="transit-mode row"> ${travel_mode}</div>`;
        }

        if (duration_text && distance_text) {
            content += `<div class="transit-duration row">${duration_text}&nbsp;&nbsp;&nbsp;&nbsp;${distance_text}</div>`;
        }

        if (travel_mode == "TRANSIT") {
            content += renderTransitStepCard(step, index);
            // content +=  `<div class="transit-num-stops row">${step.transit_details.num_stops}</div>`;
        }

        content += '</div></div>'
        return content;
    }



    function displayJourneySteps(steps) {
        content = '';
        stepLength = steps.length;

        $.each(steps, function (index, step) {

            var travel_mode = (step || {}).travel_mode,
                transit_details = (step || {}).transit_details;

            if (travel_mode == "TRANSIT") {
                if (transit_details) {

                    var departure_time_text = ((transit_details || {}).departure_time || {}).text,
                        departure_stop_name = ((transit_details || {}).departure_stop || {}).name,
                        departure_stop_location = ((transit_details || {}).departure_stop || {}).location,
                        arrival_time_text = ((transit_details || {}).arrival_time || {}).text,
                        arrival_stop_name = ((transit_details || {}).arrival_stop || {}).name,
                        arrival_stop_location = ((transit_details || {}).arrival_stop || {}).location;

                    //check if the keys exist in the step object
                    if (departure_time_text
                        && departure_stop_name
                        && departure_stop_location
                        && arrival_time_text
                        && arrival_stop_name
                        && arrival_stop_location) {
                        content += renderTransitStop(departure_time_text,
                            departure_stop_name,
                            departure_stop_location);
                        content += renderTransitDetail(step, index);
                        content += renderTransitStop(arrival_time_text,
                            arrival_stop_name,
                            arrival_stop_location);
                    }
                }
            } else {
                content += renderTransitDetail(step, index);
            }

            var points = ((step || {}).polyline || {}).points,
                end_location_lat = ((step || {}).end_location || {}).lat,
                end_location_lng = ((step || {}).end_location || {}).lng;

            if (points) {
                var coordinates = decode(points);
                drawPolylineOnMap(travel_mode, coordinates);
            }

            if (index !== (stepLength - 1) && end_location_lat && end_location_lng) {
                //drop destination marker
                dropMarkerOnMap(end_location_lat, end_location_lng, "", "circle");
            }
        });

        $("#journey-result-steps").append(content);
    }



    function renderTransitStepCard(step, index) {

        content = "";

        // Using the card component, show the steps of journey on card header
        // show detail of each step in card body 
        // resource: https://getbootstrap.com/docs/4.0/components/collapse/
        content += `
        <div class="card" style="margin: 10px 0px;"> 
        <div class="card-header" id="heading-${index}"><h5 class="mb-0">
        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-${index}" aria-expanded="false" aria-controls="collapse-${index}">`;

        //check if short_name and stops exist in json object
        var short_name = (((step || {}).transit_details || {}).line || {}).short_name,
            stops = ((step || {}).transit_details || {}).stops,
            html_instructions = (step || {}).html_instructions;


        if (short_name) {
            content += `<div class="transit-bus-line row">Route ${short_name}`
        }

        if (stops) {
            content += `&nbsp;&nbsp;&nbsp;&nbsp<b> ${stops.length}</b> stops</div>`;
        }

        // add journey steps detail in card body
        content += `
        </button></h5></div>
        <div id="collapse-${index}" class="collapse" aria-labelledby="heading-${index}" data-parent="#journey-result-steps">
        <div class="card-body">`;

        if (stops) {
            $.each(stops, function (index, value) {
                content += "<p> " + value.plate_code + "  " + value.stop_name + "</p>";
            });
        } else {
            if (html_instructions) {
                content += "<p>" + html_instructions + "</p>";
            }
        }
        content += '</div></div></div>';

        return content;
    }



    function renderContent(obj) {
        content = '<p>';
        $.each(obj, function (key, value) {
            content += key;
            content += '  ';
            content += value;
            content += '<br>'
        });
        content += '</p>';
        return content
    }



    function dropMarkerOnMap(lat, lon, location = "", markerShape = "default") {

        if (markerShape == "circle") {
            var marker = new L.CircleMarker([lat, lon], {
                radius: 10,
                color: '#FF0000'
            });
        } else {
            var marker = L.marker([lat, lon]);
        }

        if (location != "") {
            marker.bindPopup(`<b> ${location}</b>`)
        }

        journeyLayer.addLayer(marker);
    }


    function drawPolylineOnMap(travel_mode, points) {

        if (travel_mode == "TRANSIT") {
            var polyline = L.polyline(points, { color: 'red' });
        } else {
            var polyline = L.polyline(points, { color: 'red', dashArray: '6, 6', dashOffset: '1' });
        }

        journeyLayer.addLayer(polyline);
        // zoom the map to the polyline
        currentBounds = polyline.getBounds()
        map.fitBounds(currentBounds);
    }


    function clearSearchResult() {

        $("#journey-result-from").empty();
        $("#journey-result-to").empty();
        $("#journey-result-datetime").empty();
        $("#section-trip-summary").empty();
        $("#journey-result-steps").empty();
        $("#journey-result-detail").empty();

        clearMapLayers()
    }


    function clearMapLayers() {
        journeyLayer.clearLayers();
        stopsLayer.clearLayers();
    }


    function showSearchJourneyDiv(time) {
        $("#journey-search-div").fadeIn(time);
        $("#journey-result-div").fadeOut(time);

    }


    function showResultJourneyDiv(time) {
        $("#journey-result-div").fadeIn(time);
        $("#journey-search-div").fadeOut(time);

    }


    // decoding encode polyline which get from google direction API
    // decode encode polyline to array which storing all points [lat,lng]
    // code from: https://gist.github.com/ismaels/6636986
    function decode(encoded) {

        // array that holds the points
        var points = []
        var index = 0, len = encoded.length;
        var lat = 0, lng = 0;
        while (index < len) {
            var b, shift = 0, result = 0;
            do {
                b = encoded.charAt(index++).charCodeAt(0) - 63;//finds ascii                                                                                    //and substract it by 63
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            var dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lat += dlat;
            shift = 0;
            result = 0;
            do {
                b = encoded.charAt(index++).charCodeAt(0) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            var dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lng += dlng;
            points.push([(lat / 1E5), (lng / 1E5)])
        }
        return points
    }
}