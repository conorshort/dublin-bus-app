$(function(){
    var tableContent=document.createElement("div");
    // var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var routesArr = cookiemonster.get('routesList');
    // document.body.appendChild(tableContent);
    var star1;

    for (let i = 0; i<routesArr.length; i++){
        // var count = i+1;
        let route = routesArr[i];
        var routeElement=document.createElement("span");
        routeElement.setAttribute('class','col-1');
        var text=document.createTextNode(route);
        routeElement.appendChild(text);
        star1=document.createElement("i");
        star1.setAttribute('class','fas fa-star starSolid');
        tableContent.appendChild(routeElement);
        tableContent.appendChild(star1);
        document.getElementById("FavouriteResult").appendChild(tableContent);
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


});

$(function(){
    var tableContent=document.createElement("div");
    // var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var journeyArr = cookiemonster.get('journeyList');
    // document.body.appendChild(tableContent);
    var star2;

    for (let i = 0; i<journeyArr.length; i++){
        // var count = i+1;   
        let journey = journeyArr[i];
        var journeyElement=document.createElement("span");
        journeyElement.setAttribute('class','col-1');
        var text=document.createTextNode(journey);
        journeyElement.appendChild(text);
        star2=document.createElement("i");
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
        // tableContent += "<tr><td style='text-align: center; vertical-align: middle;'>"+"<span class='col-1'><i class='fas fa-star starSolid' ></i></span>"+route+ "</td></tr>";
    }
    // tableContent += "</table>";

    $("#FavouriteResult2").html(tableContent);


});
