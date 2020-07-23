
    //    $('.star').click(function(e){
    //        alert("hihi");
    //        e.preventDefault;
    //        var stop = [];
    //        if (document.getElementById("stop_id").value === ""){
    //            alert('please input stop')
    //        }
    //        else{
    //            stop.push(document.getElementById("stop_id").value);
    //            $(this).toggleClass("fa fa-star fa fa-star");
    //            try{
    //                cookiemonster.get('stop');
    //                cookiemonster.append('stop', stop, 3650);
    //            } catch(err){
    //                cookiemonster.set('stop', stop, 3650);
    //            }
    //            alert('Save Sucessfully');
    //        }
    //    });

 
    //    $(function(){
    //        $("#favourite").click(function(e){
    //        $("#FavouriteResult").html("");
    //        // alert("hi");
    //        var tableContent = "<br>";
    //        var stopArr = cookiemonster.get('stop');
          
    //        for (let i = 0; i<stopArr.length; i++){
    //            var count = i+1;
    //            let stop = stopArr[i];
    //            // console.log(stop);
    //            tableContent += stop;
    //            console.log(tableContent);
    //        }
    //        $("#FavouriteResult").html(tableContent);
    //    });
    //    });
      



// $(document).ready(function(){  
//     $.ajaxSetup({  
//         data: {csrfmiddlewaretoken: '{{ csrf_token }}' },  
//     });

// $('.star').click(function(){  

//     alert("hi");
//     info={      
//             csrfmiddlewaretoken: '{{csrf_token}}',
//             route: $('route-item').val(),
//          };

//         $.ajax({  
//             type:"POST",  
//             cache: false,  
//             // dataType: "html",  
//             // headers:{'Content-Type':"application/json"},
//             data: info,
//             url: "http://127.0.0.1:8000/set_cookie/", //url to handle variables
//             success: function(result, statues, xml){  
//                 // if success, return the result back to html with id "#leap-info"
//                 console.log(result);
//                 alert('Save Successfully'); 
//             },  
//             error: function(){  
//                 //otherwise alert false
//                 alert("false");  
//             }  
//         });  
//         return false;  
//     });  
// });

// $('#favourite').submit(function(){  
//     //info is getting username and password values by their id
//     alert("hi");

//         $.ajax({  
//             type:"GET",  
//             cache: false,  
//             // dataType: "html",  
//             // headers:{'Content-Type':"application/json"},
//             data: info,
//             url: "http://127.0.0.1:8000/get_cookie/", //url to handle variables
//             success: function(result, statues, xml){  
//                 // if success, return the result back to html with id "#leap-info"
//                 console.log(result);
//                 $("#FavouriteResult").html(result);
//             },  
//             error: function(){  
//                 //otherwise alert false
//                 alert("false");  
//             }  
//         });  
//         return false;  
//     });  
// });