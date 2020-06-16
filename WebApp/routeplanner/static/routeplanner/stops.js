$.getJSON('http://127.0.0.1:8000/api/stops/nearby?longitude=-6.263695&latitude=53.3522411111&radius=0.1', function(data) {
        console.log(data);
        content = '';
        $.each(data, function (i, stop) {
            content += renderListItem(stop);
            showStopsOnMap(stop)
        });
        console.log(content);
        $( "#stopsListGroup" ).append(content);
});

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
    L.marker([stop.latitude, stop.longitude]).addTo(mymap);
}


    // $('#test').click(function(e) {  
//     
// });



