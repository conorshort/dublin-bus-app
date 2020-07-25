
$(function(){
    var tableContent = "<table style='width:100%'><tr style='border-bottom:1pt solid black;'><th style='text-align: center; vertical-align: middle;'>favourite routes</th></tr>";
    var routesArr = cookiemonster.get('routesList');
    for (let i = 0; i<routesArr.length; i++){
        var count = i+1;
        let route = routesArr[i];

        tableContent += "<tr><td style='text-align: center; vertical-align: middle;'>"+"<span class='col-1'><i class='fas fa-star starSolid' ></i></span>"+route+ "</td></tr>";
    }
    tableContent += "</table>";
    $("#FavouriteResult").html(tableContent);


});
// thisRoute='${route}

$('.starSolid').click(function(e){
    alert('hil');
    e.preventDefault;
    let addedRoute = $(this).attr("thisRoute");
    // var routesList = [];
    // routesList.push(starredRoute);
    // $(this).toggleClass("fa fa-star fa fa-star");
    // alert(routesList);

    try{
        let routess = cookiemonster.get('routesList')
        for (let i=0;i<routess.length;i++){
            if(routess[i]===addedRoute.value){
                cookiemonster.splice(outesList, i, 1, 3650);
        
    }}} catch(err){
        cookiemonster.splice(addedRoute, 1, 1, 3650);
    }
    alert('remove Sucessfully');
});