$(document).ready(function () {
    twttr.widgets.load()

    //hide loader
    $("#journey-loader").hide();

    //clear all markers and polyline on the map
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();

    //init datetime picker
    document.getElementsByClassName("datetimeInput").flatpickr({
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        
        //set datetime picker default value to current datetime
        onReady: function (selectedDates, dateStr, instance) {
            $('.datetimeInput').val(
                instance.formatDate(new Date(), "Y-m-d H:i")
            )
        },
    });　

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


        autocomplete.addListener('place_changed', function() {

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

    initAutocomplete(form_input);
    initAutocomplete(to_input);
    
}


// submit button click event 
$('form').submit(function(e){

    //show loader when click submit btn
    $("#journey-loader").show();

    // Stop form refreshing page on submit
    e.preventDefault();

    var origin = document.forms["journeyForm"]["f_from_stop"].value;
    var destination = document.forms["journeyForm"]["f_to_stop"].value;
    var dateTime =document.querySelector(".datetimeInput").value;

    var dt = new Date(Date.parse(dateTime));
    //set departure time mins to 0,
    //if departure time given is 
    dt.setMinutes(0);
    var unix = dt.getTime()/1000;

    //get direction from api /api/direction
    $.getJSON(`http://127.0.0.1:8000/api/direction?origin=${origin}&destination=${destination}&departureUnix=${unix}`
    , function(data) {
        console.log(data)
        if (data.status == "OK"){
            try {
                var route = data.routes[0];
                var leg = route.legs[0];
                var arrive_time =  leg.arrival_time.text;
                var departure_time =  leg.departure_time.text;
                var renderSteps = renderResultJourneySteps(leg.steps);
                var duration = leg.duration.text;
                var transferCount = ((renderSteps.match(/bus_icon/g) || []).length).toString() ;
                
                // render duration and count of transfer 
                var detail = renderContent({"Total duration:" : "<b>" + duration + "</b>" 
                                                                + "&nbsp;&nbsp;&nbsp;&nbsp;" 
                                                                + "<b>" + transferCount + "</b>" 
                                                                + "  transfers"});
                                        
                // dictionary to store all the elements which are going to display on frontend
                // key: the element id or class name
                // value: content to append to the element 
                var obj = {
                    "#journey_result_from" : origin,
                    "#journey_result_to" : destination,
                    "#journey_result_datetime" : dateTime,
                    "#journey_result_travel_time" : departure_time + " &nbsp;&nbsp; <b style='font-size: 30px;'> &#8250; </b>  &nbsp;&nbsp;" + arrive_time,
                    "#journey_result_steps" : renderSteps,
                    "#journey_result_detail" : detail
                };
                displayElements(obj);

                //get encoding journey polyline
                var encodingPolyline = route.overview_polyline.points;
                //decode polyline to latlngs array
                var coordinates = decode(encodingPolyline);
                
                drawPolylineOnMap(coordinates);
                //drop destination marker
                dropMarkerOnMap(leg.end_location.lat, leg.end_location.lng, leg.end_address);
                //drop origin marker
                dropMarkerOnMap(leg.start_location.lat, leg.start_location.lng, leg.start_address);

                showResultJourneyDiv();
                
            } catch (error) {
                
                alert(error);
            }
        } else {
            alert("No journey planning result, please try input other locations.");
        }

        //hide loader
        $("#journey-loader").hide();
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


// render result journey steps
function renderResultJourneySteps(steps) {
    //  TODO: handling when no bus journey, steps will become 0

    content = '';
    $.each( steps, function( index, step ) {

        // Using the card component, show the steps of journey on card header
        // show detail of each step in card body 
        // resource: https://getbootstrap.com/docs/4.0/components/collapse/
        content += `
            <div class="card"> 
            <div class="card-header" id="heading${index}"><h5 class="mb-0">
            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">`;
    
        // if the travel_mode is TRANSIT, add bus icon and bus route number to content
        if (step.travel_mode == "TRANSIT"){
            var line = step.transit_details.line;
            content +=  `<img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon"> &nbsp;`;
            content += line.short_name;

        // if the travel_mode is WALKING, add walk icon to content
        } else if (step.travel_mode == "WALKING") {
            content +=  `<img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon"> Walking`;
        }

        // add duration for the step to content
        content += " (" + step.duration.text + ") ";

        // add journey steps detail in card body
        content += `
            </button></h5></div>
            <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#journey_result_steps">
            <div class="card-body">`;
        content += "<p>Distance: <b>" + step.distance.text + "</b></p>";
        // if the travel_mode is TRANSIT, add bus icon and bus route number to content
        if (step.travel_mode == "TRANSIT"){
            
            //show number of stops
            content += "<p> <b>" + step.transit_details.num_stops + " Stops</b></p>";

            var stops = step.transit_details.stops;

            if (stops) {
                
                $.each(stops, function( index, value ) {
                    content += "<p> " + value.plate_code + "  " + value.stop_name + "</p>";
                });
            }


        // if the travel_mode is WALKING, add walk icon to content
        } else if (step.travel_mode == "WALKING") {
            content += "<p>" + step.html_instructions + "</p>";
        }
        content += '</div></div></div>';
      
    });
    return content
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


function dropMarkerOnMap(lat, lon, location){
 
    var marker = L.marker([lat, lon]) .bindPopup(`<b> ${location}</b>`);
    journeyLayer.addLayer(marker);
}


function drawPolylineOnMap(points){
    var polyline = L.polyline(points, {color: 'red'});
    journeyLayer.addLayer(polyline);
    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
}


function clearSearchResult(){
    var obj = {
        "#journey_result_from" : "",
        "#journey_result_to" : "",
        "#journey_result_datetime" : "",
        "#journey_result_travel_time" : "",
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