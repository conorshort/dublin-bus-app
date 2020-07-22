$(document).ready(function () {

    //clear all markers and polyline on the map
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();

    showSearchJourneyDiv();
    initAutoComplete();
});


function initAutoComplete(){

    //add restriction for autocomplete places API
    var options = {
        componentRestrictions: {country: "IE"}
    };

    var form_input = document.getElementById('form_input');
    var to_input = document.getElementById('to_input');

    function initAutocomplete(input){

        //use Google Place Autocomplete for input box
        //source: https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
        var autocomplete = new google.maps.places.Autocomplete(input, options);

        // Set the data fields to return when the user selects a place.
        autocomplete.setFields(
            ['address_components', 'geometry', 'icon', 'name']);

        var infowindow = new google.maps.InfoWindow();
        var infowindowContent = document.getElementById('infowindow-content');
        infowindow.setContent(infowindowContent);
    

        autocomplete.addListener('place_changed', function() {
        infowindow.close();

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

        infowindowContent.children['place-icon'].src = place.icon;
        infowindowContent.children['place-name'].textContent = place.name;
        infowindowContent.children['place-address'].textContent = address;
        });
    }

    initAutocomplete(form_input);
    initAutocomplete(to_input);
    
}


// submit button click event 
$('form').submit(function(e){
    // Stop form refreshing page on submit
    e.preventDefault();

    var origin = document.forms["journeyForm"]["f_from_stop"].value;
    var destination = document.forms["journeyForm"]["f_to_stop"].value;
    var dateTime = document.querySelector('input[type="datetime-local"]').value;

    // var origin = 'dundrum';
    // var destination = 'dun la';
    // var dateTime = '20';

    var dt = new Date(Date.parse(dateTime));
     //set departure time mins to 0,
    //if departure time given is 
    dt.setMinutes(0);
    var unix = dt.getTime()/1000;

    //get direction from api /api/direction
    $.getJSON(`http://127.0.0.1:8000/api/direction?origin=${origin}&destination=${destination}&departureUnix=${unix}`
    , function(data) {
        console.log(data);
        if (data.status == "OK"){
            try {
                var route = data.routes[0];
                var leg = route.legs[0];
                var arrive_time =  leg.arrival_time.text;
                var departure_time =  leg.departure_time.text;
                var duration = leg.duration.text;
                // var transferCount = ((renderSteps.match(/bus_icon/g) || []).length).toString() ;
                
                displaySearchInfoOnHeader(origin, destination, dateTime);
                displayTripSummary(duration, '0', departure_time, arrive_time);


                //render and append origin waypoint
                var origin_waypoint = renderTransitStop(departure_time, leg.start_address, leg.start_location);
                appendElements({"#journey_result_steps" : origin_waypoint});

                displayJourneySteps(leg.steps);

                //render and append origin waypoint
                var destination_waypoint = renderTransitStop(arrive_time, leg.end_address, leg.end_location);
                appendElements({"#journey_result_steps" : destination_waypoint});

                //drop origin marker
                dropMarkerOnMap(leg.start_location.lat, leg.start_location.lng, leg.start_address);
                //drop destinaiton marker
                dropMarkerOnMap(leg.end_location.lat, leg.end_location.lng, leg.end_address);

                showResultJourneyDiv();

            } catch (error) {
                alert(error);
            }
        } else {
            alert("No journey planning result, please try input other locations.");
        }   
    });
});



$('#edit_journey_input').click(function () {
    showSearchJourneyDiv();
    clearSearchResult();

});



//append value to key element
function displayElements(obj){
    $.each( obj, function( key, value ) {
        $(key).html(value);
    });
}

//append value to key element
function appendElements(obj){
    $.each( obj, function( key, value ) {
        $(key).append(value);
    });
}



function displaySearchInfoOnHeader(origin, destination, dateTime){
    // dictionary to store all the elements which are going to display on frontend
    // key: the element id or class name
    // value: content to append to the element 
    var obj = {
        "#journey_result_from" : origin,
        "#journey_result_to" : destination,
        "#journey_result_datetime" : dateTime
    };
    displayElements(obj);
}

function displayTripSummary(duration, transferCount, departure_time, arrive_time){
    // dictionary to store all the elements which are going to display on frontend
    // key: the element id or class name
    // value: content to append to the element 
    // render duration and count of transfer 
    var duration_tranfer_count = renderContent({"Total duration:" : "<b>" + duration + "</b>" 
                                + "&nbsp;&nbsp;&nbsp;&nbsp;" 
                                + "<b>" + transferCount + "</b>" 
                                + "  transfers"});

    var obj = {
        "#journey_result_detail" : duration_tranfer_count,
        "#section-trip-summary" : departure_time + " &nbsp;&nbsp; <b style='font-size: 30px;'> &#8250; </b>  &nbsp;&nbsp;" + arrive_time,
                    
    };
    displayElements(obj);

}




function renderTransitStop(timeline, name, coordinates){
    content = '<div class="transit-stop row" style="margin:0px; padding:0px;"> ';
    content += `<div class="transit-timeline col-3" style="text-align:right; ">${timeline}</div>`
    content += '<div class="col-1" style="margin:0px; padding:0px;"><div style="background: red; border-radius: 50%; width: 24px; height: 24px; margin-left: -3px;"></div></div>';
    content += `<div class="transit-stop-name col-8" style="margin:0px; padding:0px;"><b>${name}</b></div>`;
    content += '</div>'

    return content;
}




function renderTransitDetail(step, index){

    content = '<div class="transit-stop row"> ';
    
    if (step.travel_mode == "TRANSIT"){
        content += `<div class="transit-timeline col-3" style="text-align:right;"><img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon"></div>`
        content += '<div class="col-1"><div style="border-left: 4px solid red; height: 100%;position: absolute;left: 50%; margin-left: -2px; top: 0;"></div></div>';

    } else {
        content += `<div class="transit-timeline col-3" style="text-align:right";><img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon"></div>`
        content += '<div class="col-1"><div style="border-left: 4px dotted red; height: 100%;position: absolute;left: 50%; margin-left: -2px; top: 0;"></div></div>';
    }

    content +=  '<div class="transit-detail col-8" style="padding-top: 20px; padding-bottom: 20px;">';
    content +=  `<div class="transit-mode row"> ${step.travel_mode}</div>`;
    content +=  `<div class="transit-duration row">${step.duration.text}&nbsp;&nbsp;&nbsp;&nbsp;${step.distance.text}</div>`;

    if (step.travel_mode == "TRANSIT"){
        content += renderStepCard(step, index);
        // content +=  `<div class="transit-num-stops row">${step.transit_details.num_stops}</div>`;
    }

    content += '</div></div>'

    return content;
}



function displayJourneySteps(steps){
    content = '';
    $.each( steps, function( index, step ) {

        if (step.travel_mode == "TRANSIT"){

            var transit_details = step.transit_details;
            content += renderTransitStop(transit_details.departure_time.text, 
                transit_details.departure_stop.name,
                transit_details.departure_stop.location);

            content += renderTransitDetail(step, index);

            content += renderTransitStop(transit_details.arrival_time.text, 
                transit_details.arrival_stop.name,
                transit_details.arrival_stop.location);


        } else if (step.travel_mode == "WALKING") {
            content += renderTransitDetail(step, index);
        }

        //get encoding journey polyline
        var encodingPolyline = step.polyline.points;
        //decode polyline to latlngs array
        var coordinates = decode(encodingPolyline);
        
        drawPolylineOnMap(step.travel_mode, coordinates);

        if (index !== (length - 1)) {
            //drop destination marker
            dropMarkerOnMap(step.end_location.lat, step.end_location.lng);
        }
        
    });

    appendElements({"#journey_result_steps" : content});
}



function renderStepCard(step, index){

    content = "";

    
    // Using the card component, show the steps of journey on card header
    // show detail of each step in card body 
    // resource: https://getbootstrap.com/docs/4.0/components/collapse/
    content += `
        <div class="card" style="margin: 10px 0px;"> 
        <div class="card-header" id="heading${index}"><h5 class="mb-0">
        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">`;

    content +=  `<div class="transit-bus-line row">Route ${step.transit_details.line.short_name}&nbsp;&nbsp;&nbsp;&nbsp;<b> ${step.transit_details.num_stops}</b> stops </div>`;   
    content +=  `<div class="transit-num-stops row"> </div>`;

     
    // add journey steps detail in card body
    content += `
        </button></h5></div>
        <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#journey_result_steps">
        <div class="card-body">`;


    // if the travel_mode is TRANSIT, add bus icon and bus route number to content
    var stops = step.transit_details.stops;

   if (stops) {
        $.each(stops, function( index, value ) {
            content += "<p> " + value.plate_code + "  " + value.stop_name + "</p>";
        });

        //show number of stops
        content += "<p>Stops: <b>" + stops.length + "</b></p>";
    } else {
        content += "<p>" + step.html_instructions + "</p>";
    }
    content += '</div></div></div>';
    
    return content;

}



function renderContent(obj){ 
    content = '<p>';
    $.each( obj, function( key, value ) {
        content += key;
        content += '  ';
        content += value;
        content += '<br>'
    });
    content += '</p>';
    return content
}


function dropMarkerOnMap(lat, lon, location=""){
 
    var marker = L.marker([lat, lon]);

    if (location != ""){
        marker.bindPopup(`<b> ${location}</b>`)
    }

    journeyLayer.addLayer(marker);
}


function drawPolylineOnMap(travel_mode, points){

    if (travel_mode == "TRANSIT"){
        var polyline = L.polyline(points, {color: 'red'});
    } else {
        var polyline = L.polyline(points, {color: 'red',  dashArray: '6, 6', dashOffset: '1'});
    }

    
    journeyLayer.addLayer(polyline);
    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
}


function clearSearchResult(){
    var obj = {
        "#journey_result_from" : "",
        "#journey_result_to" : "",
        "#journey_result_datetime" : "",
        "#section-trip-summary" : "",
        "#journey_result_steps" : "",
        "#journey_result_detail" : ""
    };

    displayElements(obj);
    journeyLayer.clearLayers();
    stopsLayer.clearLayers();
}


function showSearchJourneyDiv(){
    $("#journey_result_div").fadeOut(10);
    $("#journey_search_div").fadeIn(10);
}

function showResultJourneyDiv(){
    $("#journey_search_div").fadeOut(10);
    $("#journey_result_div").fadeIn(10);
}


// decoding encode polyline which get from google direction API
// decode encode polyline to array which storing all points [lat,lng]
// code from: https://gist.github.com/ismaels/6636986
function decode(encoded){

    // array that holds the points

    var points=[ ]
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
 
   points.push([(lat / 1E5), ( lng / 1E5)])  
 
  }
  return points
}