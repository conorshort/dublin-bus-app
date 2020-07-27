//show the routes in favourite page and remove it when clicked solid star
$(function(){
    $('#fav_routes').click(function(){

        //hide other two tables when routes is click in nav bar
        $('#stopsTable').hide();
        $('#journeyTable').hide();

    var tableContent=document.createElement("div");
    tableContent.setAttribute('id','routesTable');
    // var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var routesArr = cookiemonster.get('routesList');
    // document.body.appendChild(tableContent);

    for (let i = 0; i<routesArr.length; i++){

        //for each route in routes list add it to a table
        let route = routesArr[i];
        var routeElement=document.createElement("span");
        routeElement.setAttribute('class','col-1');
        var text=document.createTextNode(route);
        routeElement.appendChild(text);
        var star1=document.createElement("i");
        star1.setAttribute('class','fas fa-star starSolid');
        tableContent.appendChild(routeElement);
        tableContent.appendChild(star1);
        document.getElementById("FavouriteResult").appendChild(tableContent);


        //remove route in the cookies when star is clicked
        star1.addEventListener('click',function(){
            alert('the item is removed from favourites');
            
            var addedRoute = cookiemonster.get('routesList');
            for (let j=0;j<routesArr.length;j++){
                if (addedRoute[j]===routesArr[i]){
                    cookiemonster.splice('routesList',i,1,3650);
                }
            }
            

        })
        // tableContent += "<tr><td style='text-align: center; vertical-align: middle;'>"+"<span class='col-1'><i class='fas fa-star starSolid' ></i></span>"+route+ "</td></tr>";
    }
    // tableContent += "</table>";

    $("#FavouriteResult").html(tableContent);
})

});


//show the journeys in favourite page and remove it when clicked solid star
$(function(){
    $('#fav_journey').click(function(){
        $('#routesTable').hide();
        $('#stopsTable').hide();
    var tableContent=document.createElement("div");
    tableContent.setAttribute('id','journeyTable');
    // var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var journeyArr = cookiemonster.get('journeyList');
    // document.body.appendChild(tableContent);

    for (let i = 0; i<journeyArr.length; i++){
        // var count = i+1;   
        let journey = journeyArr[i];
        var journeyElement=document.createElement("span");
        journeyElement.setAttribute('class','col-1');
        var text=document.createTextNode(journey);
        journeyElement.appendChild(text);
        var star2=document.createElement("i");
        star2.setAttribute('class','fas fa-star starSolid');
        tableContent.appendChild(journeyElement);
        tableContent.appendChild(star2);
        document.getElementById("FavouriteResult2").appendChild(tableContent);
        star2.addEventListener('click',function(){
            alert('the item is removed from favourites');
            
            var addedJourney = cookiemonster.get('journeyList');
            for (let j=0;j<journeyArr.length;j++){
                if (addedJourney[j]===journeyArr[i]){
                    cookiemonster.splice('journeyList',i,1,3650);
                }
            }
            
        })
        var breakk=document.createElement("br");
        tableContent.appendChild(breakk);
        // tableContent += "<tr><td style='text-align: center; vertical-align: middle;'>"+"<span class='col-1'><i class='fas fa-star starSolid' ></i></span>"+route+ "</td></tr>";
    }
    // tableContent += "</table>";

    $("#FavouriteResult").html(tableContent);

    })
});


//show the stops in favourite page and remove it when clicked solid star
$(function(){
    $('#fav_stop').click(function(){
        $('#routesTable').hide();
        $('#journeyTable').hide();
    var tableContent=document.createElement("div");
    tableContent.setAttribute('id','stopsTable');
    // var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var stopsArr = cookiemonster.get('stopsList');
    // document.body.appendChild(tableContent);

    for (let i = 0; i<stopsArr.length; i++){
        // var count = i+1;   
        let stops = stopsArr[i];
        var stopsElement=document.createElement("span");
        stopsElement.setAttribute('class','col-1');
        var text=document.createTextNode(stops);
        stopsElement.appendChild(text);
        var star3=document.createElement("i");
        star3.setAttribute('class','fas fa-star starSolid');
        tableContent.appendChild(stopsElement);
        tableContent.appendChild(star3);
        document.getElementById("FavouriteResult3").appendChild(tableContent);
        star3.addEventListener('click',function(){
            alert('the item is removed from favourites');
            
            var addedstops = cookiemonster.get('stopsList');
            for (let j=0;j<stopsArr.length;j++){
                if (addedstops[j]===stopsArr[i]){
                    cookiemonster.splice('stopsList',i,1,3650);
                }
            }
            
        })
        var breakk=document.createElement("br");
        tableContent.appendChild(breakk);
        // tableContent += "<tr><td style='text-align: center; vertical-align: middle;'>"+"<span class='col-1'><i class='fas fa-star starSolid' ></i></span>"+route+ "</td></tr>";
    }
    // tableContent += "</table>";

    $("#FavouriteResult").html(tableContent);

    })
});


