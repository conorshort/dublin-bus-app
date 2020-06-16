
// console.log(`http://127.0.0.1:8000/api/stops/nearby?latitude=${centreLocation[0]}&longitude=${centreLocation[1]}&radius=0.5`);
$.getJSON(`http://127.0.0.1:8000/api/stops/nearby?latitude=${centreLocation[0]}&longitude=${centreLocation[1]}&radius=0.5`, function(data) {
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
    .addTo(map)
    .bindPopup(`<b> ${stop.fullname}</b> <br> ${stop.routes}`);
}




