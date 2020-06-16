$.getJSON('http://127.0.0.1:8000/api/stops/nearby?longitude=-6.263695&latitude=53.3522411111&radius=0.1', function(data) {
        content = '';
        $.each(data, function (i, stop) {
            content += renderListItem(stop);
            showStopsOnMap(stop)
        });
        $( "#stopsListGroup" ).append(content);
});

// create and return list-group-item for stop
function renderListItem(stop) {
    const content = `
    <li class="list-group-item" id="station-${stop.stopid}">
        <ul>
            <li><b>${ stop.fullname }</b></li>
            <li>${ stop.routes }</li>
        </ul>
    </li>`;
    return content;
}

function showStopsOnMap(stop) {
    L.marker([stop.latitude, stop.longitude])
    .addTo(mymap)
    .bindPopup(stop.fullname + "<br>" + stop.routes);;
}


$('.list-group-item').click(function(e) {  

});



