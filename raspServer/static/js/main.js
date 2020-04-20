
(function ($) {
    "use strict";

        
    

})(jQuery);

let changeName = function() {
    let xttp = new XMLHttpRequest();
    xttp.onreadystatechange = function() {
        showAlert(xttp.response);
      }
    const sensor_id = document.getElementById('sensorNameBox').value;
    const new_name = document.getElementById('nodeKeyText').value;
    const request_url = 'http://127.0.0.1:8000/sensors/'+sensor_id+'/'+new_name
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    xttp.open('POST', request_url, false);
    xttp.setRequestHeader("X-CSRFToken", csrftoken);
    xttp.send();
}

let showAlert = function(response){
    alert('New name saved.');
    location.reload();
}