$(document).ready(function () {
    $("#journey_result_div").fadeOut(10);
    $("#journey_search_div").fadeIn(10);

    // var encodingPolyline = "czfdIjebe@EJKBMMEPM\\y@vAwBlB_@XESDR^Yf@a@DJDR@`@?|AFjB|@`FXr@V`@HCJDDNxAPtBFnAIpB{@dCKbAIpJqCbA[|B{@fAc@FMFOBMLg@Ke@F]T_@ZITFNZ@R^ZLTpHxAx@L~ATlAX@MBKLMF@B@ZQt@W|AGxABzAIp@MhC{@dGuBbBWjAAnAJdAJxADf@O^e@@ONa@ZWXAXPHJn@FXQRMp@c@AMAS@QJc@TWVERJNZHj@Cf@_@bBAz@LdA\\vAlA~ExAnEdEzKj@fBJp@lBhHLz@r@dFp@fHXtGCrMQlE]xDk@hE}@rEqBjJg@xCo@tEg@lHKhDA|FR~GVpDh@lEjAzGnBtJpAbJ^nFNfEDhGMtP_@lNm@tMaBdT}BfRmAhH{AhGuBlG_BrDcCpEoFtHkBnC_B|CmAvCsAhEgAxEw@fFs@xIOrEWrQWfF]xEq@nFyA`IkBzGyBzFsBtD_@l@gBbCoBxBsBfByAfA}ChBgOfHq^xPe\\lOwJzEsCbBgCnBi@\\wDtDqA|AuD`FwDtGqDbIqDhKgJj[cQ`n@eEnOyA~DsBjEoChE_DjDiAbAeCbB}F~DkFnEyEbFOp@uHvJcDfEi@|@a@`Ai@rCGbAF`CZzDCbAz@hHX~BZh@NNP@xAgATi@JoAMcAKIO@ABC@_@tAOd@l@|@UiFHOL@HRIf@KAOlAWt@w@~@aDvBaA\\Kd@U@Km@HURALsFAcDRwAOaAkBuCmA{@o@Wk@IeCBwEbCaHxE}DdCy\\|^ce@fg@eHvGgBrAaE~BmCbAaFpA}Dh@oBLkHKiu@oK}^}EiX{Eg`@wHwC{@iEsBiF_E{BeCkCwD_IsOaCoDaBoBmKwJ{DgEyM_PuKaM_GmH_HkIsG}H}G}HiDaF}B{DmDsHeBiE{CsJigA}bEsYcgA{DsRkCsPkB{O{@{IqBm\\i@gTwDksBoAkXk@mH}@uFe@_Bs@_Aw@u@sB]s@_@sCQaIRaG[oALoCx@gE~@SkBQ_AaDeIw@yBw@mDk@{EQiEE_HDsEVoG~Doq@t@qw@I}A]qAkFgJ_HgOqBkDqC{DeCkCe@Qu@k@k@SOBe@Vg@n@}DpQI|@uApGi@bBk@rFYfC{DfSy@z@]Di@_@c@o@i@So@TcAlBYa@g@KAn@GNu@DaBQF_BHEJ@Xh@ZD@yBe@Aa@@?~@FDN^XV?Z\\@~@HL?LVXp@`CzEVf@";
    // var polyline = L.Polyline.fromEncoded(encodingPolyline);
    // // var coordinates = L.polyline.fromEncoded(encodingPolyline).getLatLngs();
    // console.log(polyline.getLatLngs());
 
    // // var polyline = require('@mapbox/polyline');
    // // var coordinates = polyline.decode(encodingPolyline);
    // // console.log(coordinates);
});


function validateForm() {
    
    var f_from_stop = document.forms["myForm"]["f_from_stop"].value;
    var f_to_stop = document.forms["myForm"]["f_to_stop"].value;
    if (f_from_stop == "" || f_to_stop == "") {
      alert("Origin and destination must be filled out");
      return false;
    }
}

$('form').submit(function(e){
    // Stop form refreshing page on submit
    e.preventDefault();
    var origin = document.forms["journeyForm"]["f_from_stop"].value;
    var destination = document.forms["journeyForm"]["f_to_stop"].value;


    $.getJSON(`http://127.0.0.1:8000/api/direction?origin=${origin}&destination=${destination}`, function(data) {

        if (data.status == "OK"){
            try {
                var route = data.routes[0];
                var leg = route.legs[0];
                var arrive_time =  leg.arrival_time.text;
                var departure_time =  leg.departure_time.text;
                var renderSteps = renderResultJourneySteps(leg.steps)

                var obj = {
                    "#journey_result_from" : origin,
                    "#journey_result_to" : destination,
                    "#journey_result_datetime" : "20:00",
                    "#journey_result_travel_time" : arrive_time + "  >  " + departure_time,
                    "#journey_result_steps" : renderSteps
                };

                displayElements(obj);

                // var encodingPolyline = route.overview_polyline.points;
                // var polyline = require('@mapbox/polyline');
                // var coordinates = polyline.decode(encodingPolyline);
                // // var coordinates = google.maps.geometry.encoding.decodePath(encodingPolyline);
                // console.log(coordinates);
                // drawPolylineOnMap(coordinates);
                dropMarkerOnMap(leg.end_location.lat, leg.end_location.lng, leg.end_address);
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
    content = '';
    $.each( steps, function( index, step ) {

        if (step.travel_mode == "TRANSIT"){
            var line = step.transit_details.line;
            content +=  `<img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon">`
            content += line.short_name;
        } else if (step.travel_mode == "WALKING") {
            content +=  `<img src="./static/img/walking_small.png" alt="bus_icon" class="journey_result_icon">` 
        }
        content += " "
        content += step.duration.text;
        content += "  >  "
    });
    return content
}


function dropMarkerOnMap(lat, lon){
    var marker = 
    L.marker([lat, lon]) .bindPopup(`<b> ${location}</b>`);
    journeyLayer.addLayer(marker);
}

function drawPolylineOnMap(latlngs){
    var polyline = L.polyline(latlngs, {color: 'red'});
    journeyLayer.addLayer(polyline);
    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
}



    

    


