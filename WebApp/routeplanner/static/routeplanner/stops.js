currentBounds = undefined;
currentCentre = [53.346967, -6.259923];
MapUIControl.halfscreen();

//event will be called when map bounds change
map.on('moveend', function(e) {
    var mapCentra = map.getCenter();
    //update centreLocation to centre of the map
    centreLocation = [mapCentra["lat"], mapCentra["lng"]];

    //clear all the markers in the layer
    stopsLayer.clearLayers();
    //clear all the elements in list group
    showStops(centreLocation[0], centreLocation[1]);
 });


$(document).ready(function() {
    $("#stop-realtime-div").fadeOut(10);
    $("#stops-div").fadeIn(10);

    //clear all the markers in the layer
    stopsLayer.clearLayers();

    var mapCentra = map.getCenter();
    //update centreLocation to centre of the map
    centreLocation = [mapCentra["lat"], mapCentra["lng"]];

    showStops(centreLocation[0] ,centreLocation[1]);
    initAutoComplete();
});


$(document).on("click.stops", '.nav_item, .bottom_nav_item', function () {
    stopsLayer.clearLayers();
    map.off('moveend');
});


// Shows Stops and distances 
function showStops(lat, lng){
    $("#stop-loader").show();
    $.getJSON(`/api/stops/nearby?latitude=${lat}&longitude=${lng}&radius=1`, function(data) {
        content = '';
        $.each(data, function (i, stop) {
            // content += document.getElementById('routes-list').innerHTML = "<a href='#'><i class='far fa-star star'></a>"
            // Get distance from centre location to every stop in kilometers
            dist_kms = distance(lat, lng,stop.latitude, stop.longitude, 'K');
            dist_ms = Math.round(dist_kms*1000);
            content += renderStopListItem(stop,dist_ms);
            markStopsOnMap(stop);
        });
        $("#stop-loader").hide();
        $("#stopsListGroup").html(content);

        let visible = $(content).length;
        if (visible == 0){
            $("#no-stops-warning").show();
        } else {
            $("#no-stops-warning").hide();
        }
    });
}




function moveMapToEnteredAddress(address){
    // console.log(address)
    // console.log("MAde it to movemap")
    $.getJSON(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=AIzaSyBavSlO4XStz2_RD_fUBGwm89mQwGwYUzA`, function(data){
        var latlng = data.results[0].geometry.location;
        //map.panTo(new L.LatLng(latlng.lat, latlng.lng))
        showStops(latlng.lat, latlng.lng); 
        map.flyTo([latlng.lat, latlng.lng], 15);
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
    $("#stop-loader").show();
    //get realtime data
    $.getJSON(`/realtimeInfo/${stopid}`, function(data) {

        // parse response data to json 
        obj = JSON.parse(data)
        if (obj.errorcode == "0") {
            results = obj.results;
            content = '';
            $.each(results, function (i, bus) {
                content += renderRealtimeListItem(bus);
            });
            $("#stop-loader").hide();
            $("#stopRealtimeListGroup").html(content);
        }  
    });
}

$(document).on("click", ".star2", function() {

    //get the stop attribute associate with the selected star and push to a list
    let starredStop = $(this).attr("data-stop");
    alert(starredStop);
    var stopsList = [];
    stopsList.push(starredStop);

    //if the stop is not in the list it will be saved in cookies
    try{
        cookiemonster.get('stopsList');
    }catch{
        cookiemonster.set('stopsList', stopsList, 3650);
        alert('Save Sucessfully');
        return ;
    }

    var previous_stops = cookiemonster.get('stopsList');
    var flag = 0;

    //if selected stop already in the list wont save again
    for(let i=0;i<previous_stops.length;i++){
        if(starredStop==previous_stops[i]){
            alert('This stop is already in the list');
            flag = 1;
        }
    }

    //if it is not in the list then will append to cookies 
        if (flag==0){
            try{
                cookiemonster.get('stopsList');
                cookiemonster.append('stopsList', stopsList, 3650);
                
            } catch{
                cookiemonster.set('stopsList', stopsList, 3650);
            }
            alert('Save Sucessfully');
        }




    // $(this).toggleClass("fa fa-star fa fa-star");
    // alert(stops);

    // try{
    //     cookiemonster.get('stops');
    //     cookiemonster.append('stops', stops, 3650);
        
    // } catch(err){
    //     cookiemonster.set('stops', stops, 3650);
    // }
    // alert('Save Sucessfully');
});

// create and return list-group-item for stop
// stop_dist added as item
function renderStopListItem(stop, stop_dist,fav = false) {
    // need to do some jiggery pokery to the stop-routes to return the info without brackets or quotations
    var route_list = stop.routes;
    route_list = route_list.slice(2,-2);
    route_list = route_list.split("', '");
    // Getting routes to display as buttons for style purposes
    route_buttons = '';
    for (var i = 0; i < route_list.length; i++) {
        route_buttons += '<button type="button" class="btn btn-outline-secondary" id="stop-button">' + route_list[i] + "</button>";
    }

    let favStr = "";
    let solid = "far";
    if (fav) {
        favStr = "fav-";
        solid = "fas"
    }

    const content = `
    
    <span class="col-1">
        <a href="#">
            <i id="${favStr}star-stop-${stop}"class="${solid} far fa-star star2 stop-star" data-stop="${stop.stopid}"></i>
        </a>
    </span>
    <li class="list-group-item stop" id="station-${stop.stopid}">
        <ul class="row">
            <li class="col-8"><b>${ stop.fullname },</b> Stop ${stop.stopid}</li>
            <li class="col-4">${ stop_dist } Metres</li>
            <li class="col"> ${ route_buttons }</li>
        </ul>
    </li>`;

    return content;
}



function renderRealtimeListItem(bus) {

    const content = `
        <li class="list-group-item stop-realtime" id="route-${bus.route}">
            <ul class="row">
                <li class="col-2"><b>${ bus.route }</b></li>
                <li class="col-6">${ bus.destination }</li>
                <li class="col-4">${ bus.duetime } mins </li>
            </ul>
        </li> `; 
    return content;
}

$(document).on("click.stops", "#back-to-stops",function () {

    $("#stop-realtime-div").fadeOut(10);
    $("#stops-div").fadeIn(10);
});


function markStopsOnMap(stop) {
    // fixing the printing of array issue on marker
    var route_list = stop.routes;
    route_list = route_list.slice(2,-2);
    route_list = route_list.split("', '");

    route_buttons = ''
    for (var i = 0; i < route_list.length; i++) {
        route_buttons += `<button type="button" class="btn btn-outline-secondary" style="font-size: 10pt; padding: 2px; margin: 1px;">` + route_list[i] + "</button>";
    }

    var marker = 
    L.marker([stop.latitude, stop.longitude])
    .bindPopup(`<b> ${stop.localname}</b><br> ${route_buttons}`);
    stopsLayer.addLayer(marker);
}


//Click function for bus stop list-item
$('.list-group-flush').on('click', '.stop', function(e) {
    // Get the name of tab on the navbar that was clicked
    var id = $(this).attr('id').replace("station-", "");;
    showArrivingBusesOnSideBar(id);

    $("#stop-realtime-div").fadeIn(10);
    $("#stops-div").fadeOut(10);
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

    initAutocomplete(stops_area);
}

$(document).on("click.stops", '.star2', function (e) {
    //get the stop attribute associated with the selected star and push to a list
    let starredStopID = $(this).attr("data-stop");
    console.log(starredStopID);
    
    $.getJSON(`/api/stops/${starredStopID}`, function(data){
        var stop = JSON.parse(data);
        console.log(stop);
    });

    $.getJSON(`/api/stops/${starredStopID}`, function(data) {

        // parse response data to json 
        var starredStop = JSON.parse(data);
            
        var stopsList = [];
        stopsList.push(starredStop);

        //if the stop is not in the list it will be saved in cookies
        try {
            cookiemonster.get('stopsList');
            console.log("running cook.get in try1")
        } catch{
            cookiemonster.set('stopsList', stopsList, 3650);

            updateStopFavourites()
            console.log("Running updateStopFavourites in catch1")
            return;
        }

        var previous_stop = cookiemonster.get('stopsList');
        var flag = 0;
        var newStops = []
        // if selected stop already in the list wont save again
        for (let i = 0; i < previous_stop.length; i++) {
            if (starredStop == previous_stop[i]) {

                flag = 1;
            } else {
                newStops.push(previous_stop[i]);
            }
        }
        if (flag == 1) {
            cookiemonster.set('stopsList', newStops, 3650);
            updateStopFavourites()
            console.log("updateing stop favs after flag==1")


        } else {
            try {
                cookiemonster.get('stopsList');
                cookiemonster.append('stopsList', stopsList, 3650);
                console.log("appended to cookies w/ get")

            } catch{
                cookiemonster.set('stopsList', stopsList, 3650);
                console.log("cookie monster.set")
            }

            updateStopFavourites()
            console.log("running update Stop favs at end of fx")
        }

    });

});

function updateStopFavourites() {
    console.log("Made it into updateStopFavourites")
    $(".stop-star").removeClass("fas").addClass("far");


    let stopsList;
    try {
        stopsList = cookiemonster.get('stopsList');
    } catch{
        $("#fav-stops-div").hide();
        return;
    }


    if (stopsList.length == 0) {
        $("#fav-stops-div").hide();
        return;
    }

    //stopsList.sort((a, b) => alphanumSort(a[0], b[0]));
    var lat = centreLocation[0];
    var lng = centreLocation[1];
    var dist_kms = distance(lat, lng, stop.latitude, stop.longitude, 'K');
    var dist_ms = Math.round(dist_kms*1000);

    let content = '';
    stopsList.forEach(stop => {
        content += renderStopListItem(stop, dist_ms, fav = true);
        $("#star-stop-" + stop[0]).removeClass("far")
            .addClass("fas");
    });

    $("#fav-stops-list").html("").append(content);
    $("#fav-stops-div").show();
    console.log("fav-stops-divs-show A !!")

}