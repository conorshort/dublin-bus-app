//TO DO: Bring User to Routes info page if they click a specific route


// Stop stops from showing on other tabs
$(document).on("click.stops", '.nav_item, .bottom_nav_item', function () {
    stopsLayer.clearLayers();
    map.off('moveend');
});

currentBounds = undefined;
currentCentre = [53.346967, -6.259923];
MapUIControl.halfscreen();
$(document).ready(function() {

    //clear all the markers in the layer
    stopsLayer.clearLayers();
    showStops();
    initAutoComplete();
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
            content += renderListItem(stop);
            // content += document.getElementById('routes-list').innerHTML = "<a href='#'><i class='far fa-star star'></a>"
            // Get distance from centre location to every stop in kilometers
            dist_kms = distance(centreLocation[0],centreLocation[1],stop.latitude, stop.longitude, 'K');
            dist_ms = Math.round(dist_kms*1000);

            content += renderListItem(stop,dist_ms);
            markStopsOnMap(stop)
        });
        $( "#stopsListGroup" ).append(content);
    });
}




function moveMapToEnteredAddress(address){
    // console.log(address)
    // console.log("MAde it to movemap")
        $.getJSON(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=AIzaSyBavSlO4XStz2_RD_fUBGwm89mQwGwYUzA`, function(data){
        console.log(data);
        var latlng = data.results[0].geometry.location
        //map.panTo(new L.LatLng(latlng.lat, latlng.lng))
        map.flyTo([latlng.lat, latlng.lng], 15)
    });
}



$('form').submit(function(e){
    // Stop form refreshing page on submit
    e.preventDefault();
    //get value entered by users
    var area = document.forms["stops-area"]["stops_area"].value
    //pass value to the address finding function
    moveMapToEnteredAddress(area);
});


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

$('.star2').click(function(){
    alert('hi');
//     let starredStop = $(this).attr("data-stop");
//     alert(starredStop);
//    var stops = [];
//    routes.push(starredStop);
//    $(this).toggleClass("fa fa-star fa fa-star");
//    alert(routes);

//    try{
//        cookiemonster.get('stops');
//        cookiemonster.append('stops', routes, 3650);
       
//    } catch(err){
//        cookiemonster.set('stops', routes, 3650);
//    }
//    alert('Save Sucessfully');
//    console.log(stops);
});

// create and return list-group-item for stop
// stop_dist added as item
function renderListItem(stop, stop_dist) {
    // need to do some jiggery pokery to the stop-routes to return the info without brackets or quotations
    var route_list = stop.routes;
    route_list = route_list.slice(2,-2);
    route_list = route_list.split("', '");
    // Getting routes to display as buttons for style purposes
    route_buttons = '';
    for (var i = 0; i < route_list.length; i++) {
        route_buttons += '<button type="button" class="btn btn-info mr-1" id="stop-button">' + route_list[i] + "</button>";
      }
    const content = `
    <span class="col-1"><i class="far fa-star star2"></i></span>
    <li class="list-group-item stop" id="station-${stop.stopid}">
        <ul>
            <li><b>${ stop.fullname }</b></li>
            <li> ${ route_buttons }</li>
            <li>${ stop_dist } Metres <li>
        </ul>
    </li>`;
    return content;
}



function renderRealtimeListItem(bus) {
 
    const content = `
    <li class="list-group-item" id = "stop-info">
        <ul>
            <li><b>${ bus.route }</b> ${ bus.destination } </li>
            <li>${ bus.duetime } mins </li>
        </ul>
    </li>`;
    return content;
}

$(document).on("click.stops", "#back-to-stops",function () {
    $("#stopsListGroup").empty();
    showStops();
});


function markStopsOnMap(stop) {
    // fixing the printing of array issue on marker
    var route_list = stop.routes;
    route_list = route_list.slice(2,-2);
    route_list = route_list.split("', '");
    route_list = route_list.join(", ");
    var marker = 
    L.marker([stop.latitude, stop.longitude])
    .bindPopup(`<b> ${stop.localname}</b><br> ${route_list}`);
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

function initAutoComplete(){

    //add restriction for autocomplete places API
    var options = {
        componentRestrictions: {country: "IE"}
    };

    var form_input = document.getElementById('stops_area');

    function initAutocomplete(input){

        //use Google Place Autocomplete for input box
        //source: https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
        var autocomplete = new google.maps.places.Autocomplete(input, options);

        // Set the data fields to return when the user selects a place.
        autocomplete.setFields(
            ['address_components', 'geometry', 'icon', 'name']);

        var infowindow = new google.maps.InfoWindow();
        var infowindowContent = document.getElementById('infowindow-content-area');
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

    initAutocomplete(stops_area);
    
}