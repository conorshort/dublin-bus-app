
$(document).ready(function() {
    //clear all the markers in the layer
    stopsLayer.clearLayers();
    showStops();
});

//event will be called when map bounds change
map.on('moveend', function(e) {
    var mapCentra = map.getCenter();
    //update centreLocation to centre of the map
    centreLocation = [mapCentra["lat"], mapCentra["lng"]];

    //clear all the markers in the layer
    stopsLayer.clearLayers();
    //clear all the elements in list group
    $("#stopsListGroup").empty();
    showStops();
 });


 // Shows Stops and distances 
function showStops(){

    $.getJSON(`http://127.0.0.1:8000/api/stops/nearby?latitude=${centreLocation[0]}&longitude=${centreLocation[1]}&radius=1`, function(data) {
        content = '';
        $.each(data, function (i, stop) {
            // Get distance from centre location to every stop in kilometers
            dist_kms = distance(centreLocation[0],centreLocation[1],stop.latitude, stop.longitude, 'K');
            dist_ms = Math.round(dist_kms*1000);

            content += renderListItem(stop,dist_ms);
            markStopsOnMap(stop)
        });
        $( "#stopsListGroup" ).append(content);
    });
}

function showArrivingBusesOnSideBar(stopid){

    //get realtime data
    $.getJSON(`http://127.0.0.1:8000/realtimeInfo/${stopid}`, function(data) {

        // parse response data to json 
        obj = JSON.parse(data)
        if (obj.errorcode == "0") {
            results = obj.results;
            
            content = '';
            $.each(results, function (i, bus) {
                content += renderRealtimeListItem(bus);
            });
            $( "#stopsListGroup" ).append(content);
        }  
    });
}


// create and return list-group-item for stop
// stop_dist added as item
function renderListItem(stop, stop_dist) {
    const content = `
    <li class="list-group-item stop" id="station-${stop.stopid}">
        <ul>
            <li><b>${ stop.fullname }</b></li>
            <li>${ stop.routes }</li>
            <li>${ stop_dist } Metres <li>
        </ul>
    </li>`;
    return content;
}

function renderRealtimeListItem(bus) {
 
    const content = `
    <li class="list-group-item">
        <ul>
            <li><b>${ bus.route }</b> ${ bus.destination } </li>
            <li>${ bus.duetime } mins </li>
        </ul>
    </li>`;
    return content;
}


function markStopsOnMap(stop) {

    var marker = 
    L.marker([stop.latitude, stop.longitude])
    .bindPopup(`<b> ${stop.fullname}</b><br> ${stop.routes}`);
    stopsLayer.addLayer(marker);
}


//Click function for bus stop list-item
$('.list-group-flush').on('click', '.stop', function(e) {
        // Get the name of tab on the navbar that was clicked
        var id = $(this).attr('id').replace("station-", "");;
        showArrivingBusesOnSideBar(id);
        $("#stopsListGroup").empty();
});


// Function to calculate the distance between two points
function distance(lat1, lon1, lat2, lon2, unit) {
	if ((lat1 == lat2) && (lon1 == lon2)) {
		return 0;
	}
	else {
		var radlat1 = Math.PI * lat1/180;
		var radlat2 = Math.PI * lat2/180;
		var theta = lon1-lon2;
		var radtheta = Math.PI * theta/180;
		var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
		if (dist > 1) {
			dist = 1;
		}
		dist = Math.acos(dist);
		dist = dist * 180/Math.PI;
		dist = dist * 60 * 1.1515;
		if (unit=="K") { dist = dist * 1.609344 }
		if (unit=="N") { dist = dist * 0.8684 }
		return dist;
	}
}

