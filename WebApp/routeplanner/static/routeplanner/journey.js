$(document).ready(function () {

    stopsLayer.clearLayers();
    journeyLayer.clearLayers();
    
    $("#journey_result_div").fadeOut(10);
    $("#journey_search_div").fadeIn(10);

});




$('form').submit(function(e){

    // Stop form refreshing page on submit
    e.preventDefault();
    var origin = document.forms["journeyForm"]["f_from_stop"].value;
    var destination = document.forms["journeyForm"]["f_to_stop"].value;


    //get direction from api /api/direction
    $.getJSON(`http://127.0.0.1:8000/api/direction?origin=${origin}&destination=${destination}`, function(data) {

        if (data.status == "OK"){
            try {
                var route = data.routes[0];
                var leg = route.legs[0];
                var arrive_time =  leg.arrival_time.text;
                var departure_time =  leg.departure_time.text;
                var renderSteps = renderResultJourneySteps(leg.steps);
                var duration = leg.duration.text;
                
                var transferCount = ((renderSteps.match(/bus_icon/g) || []).length).toString() ;
                console.log(transferCount);
                var content = renderContent({"Total duration:" : "<b>" + duration + "</b>" 
                                                                    + "&nbsp;&nbsp;&nbsp;&nbsp;" 
                                                                    + "<b>" + transferCount + "</b>" 
                                                                    + "  transfers"});


                var obj = {
                    "#journey_result_from" : origin,
                    "#journey_result_to" : destination,
                    "#journey_result_datetime" : "20:00",
                    "#journey_result_travel_time" : arrive_time + " &nbsp;&nbsp; <b style='font-size: 30px;'> &#8250; </b>  &nbsp;&nbsp;" + departure_time,
                    "#journey_result_detail" : content + "<br>" + renderSteps
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

            } catch (error) {
                alert(error);
            }
        } else {
            alert("Error occur, please try again");
        }
    });

    $("#journey_search_div").fadeOut(10);
    $("#journey_result_div").fadeIn(10);

});


//append value to key element
function displayElements(obj){
    $.each( obj, function( key, value ) {
        $(key).append(value);
    });
}


// render result journey steps
function renderResultJourneySteps(steps) {
    content = '<p>';
    $.each( steps, function( index, step ) {

        if (step.travel_mode == "TRANSIT"){
            var line = step.transit_details.line;
            content +=  `<img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon">`
            content += line.short_name;
        } else if (step.travel_mode == "WALKING") {
            content +=  `<img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon">` 
        }
        content += " (";
        content += step.duration.text;
        content += ") ";
        var isLastElement = index == steps.length -1;
        if (!isLastElement) {
            content += "  &nbsp;<b style='font-size: 20px;'> &#8250; </b>&nbsp; ";
        }
    });
    content += '</p>'
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
    var marker = 
    L.marker([lat, lon]) .bindPopup(`<b> ${location}</b>`);
    journeyLayer.addLayer(marker);
}


function drawPolylineOnMap(points){
    var polyline = L.polyline(points, {color: 'red'});
    journeyLayer.addLayer(polyline);
    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
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




