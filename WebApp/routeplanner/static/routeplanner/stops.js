
$(document).ready(function() {

    // //clear all the markers in the layer
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();
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
 
function showStops(){

    $.getJSON(`/api/stops/nearby?latitude=${centreLocation[0]}&longitude=${centreLocation[1]}&radius=1`, function(data) {
        content = '';
        $.each(data, function (i, stop) {
            content += renderListItem(stop);
            // content += document.getElementById('routes-list').innerHTML = "<a href='#'><i class='far fa-star star'></a>"
            markStopsOnMap(stop)
        });
        $( "#stopsListGroup" ).append(content);
    });
}

function showArrivingBusesOnSideBar(stopid){

    //get realtime data
    $.getJSON(`/api/realtimeInfo/${stopid}`, function(data) {

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
function renderListItem(stop) {
    const content = `
    <li class="list-group-item stop" id="station-${stop.stopid}">
        <ul>
            <li><b>${ stop.fullname }</b></li>
            <li>${ stop.routes }</li>
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







