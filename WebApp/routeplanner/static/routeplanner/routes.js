



// Function for naturalsort from:
// http://web.archive.org/web/20130826203933/http://my.opera.com/GreyWyvern/blog/show.dml/1671288
// Sorts the route names in a nicer way
function alphanumSort(a, b) {
    function chunkify(t) {
        var tz = [], x = 0, y = -1, n = 0, i, j;

        while (i = (j = t.charAt(x++)).charCodeAt(0)) {
            var m = (i == 46 || (i >= 48 && i <= 57));
            if (m !== n) {
                tz[++y] = "";
                n = m;
            }
            tz[y] += j;
        }
        return tz;
    }

    var aa = chunkify(a);
    var bb = chunkify(b);

    for (x = 0; aa[x] && bb[x]; x++) {
        if (aa[x] !== bb[x]) {
            var c = Number(aa[x]), d = Number(bb[x]);
            if (c == aa[x] && d == bb[x]) {
                return c - d;
            } else return (aa[x] > bb[x]) ? 1 : -1;
        }
    }
    return aa.length - bb.length;
}


// create and return list-group-item for route
function renderListItem(route) {
    const content = `
    <li class="list-group-item route-item" id="route-${route}">
        <ul>
            <li><b>${ route}</b></li>
        </ul>
    </li>`;
    return content;
}


$.getJSON("api/routes/routename", function (data) {

    let routes = [];
    data.forEach(route => {
        routes.push(route.route_name);
    });
    routes.sort(alphanumSort);

    let content = '';
    routes.forEach(route => {
        content += renderListItem(route);
    });

    $("#routes-list").append(content);

    $(".route-item").click(function() {
        let routeName = $(this).attr('id');
        routeName = routeName.split("-")[1];
        displayRouteOnMap(routeName, 1)
    });

    $("#route-filter").keyup(function() {
        filterRouteList() })

});






function displayRouteOnMap(routeName, direction) {
    directionInbound = 1;
    console.log(routeName);
    $.getJSON("/api/shapes/geo_json/", { routename: routeName, inbound: directionInbound },
        function (data) {
            console.log(data);
            var myStyle = {
                "color": '#' + Math.floor(Math.random() * 16777215).toString(16),
                "weight": 5,
                "opacity": 0.65
            };

            L.geoJSON(data, {
                style: myStyle
            }).addTo(mymap);

        })

}


function filterRouteList() {
    // Declare variables

    var input, filter, li, a, i, txtValue;
    input = $('#route-filter');
    console.log(input);
    filter = input.val().toUpperCase();
    li = $('.route-item');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        let routeFound = false;
        a = li[i].getElementsByTagName("b")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            routeFound = true;
        } else {
            li[i].style.display = "none";
        }
    }
}