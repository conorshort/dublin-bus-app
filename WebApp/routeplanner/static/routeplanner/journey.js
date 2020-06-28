function validateForm() {
    var f_from_stop = document.forms["myForm"]["f_from_stop"].value;
    var f_to_stop = document.forms["myForm"]["f_to_stop"].value;
    if (f_from_stop == "" || f_to_stop == "") {
      alert("Origin and destination must be filled out");
      return false;
    }
}

$('#journeyForm').on('submit', function(e){
    // e.preventDefault();
    $.ajax({
       type: "POST",
       url: "/postinfo.php",
       data: $(this).serialize(),
       success: function() {
         alert('success');
       }
    });
});