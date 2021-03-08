$(document).ready(function () { 
     // This part was taken from this w3schools article on how to dynamically display the sliders value https://www.w3schools.com/howto/howto_js_rangeslider.asp
    
    if (document.getElementById("rating")) {
    let slider = document.getElementById("rating");
    let output = document.getElementById("display");
    output.innerHTML = slider.value; 
    slider.oninput = function() {
    output.innerHTML = this.value;
    }
    };
});
