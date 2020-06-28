$(document).ready(function () {
    console.log("h");
    $("#journey_result_div").fadeOut(10);
    $("#journey_search_div").fadeIn(10);
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

                displayElements(obj)

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
            content += line.vehicle.type;
            content += line.short_name;
        } else {
            content += step.travel_mode;
            
        }
        
        content += " "
        content += step.duration.text;
        content += " > "
    });
    return content
}



    

    

