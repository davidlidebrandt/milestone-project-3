$(document).ready(function () {
    $(".regnav-button, .register-link").click(function() {
        $("#login").hide();
        $("#register").show();
        $(".collapse").removeClass("show");
    });
    $(".loginnav-button, .login-link").click(function() {
        $("#register").hide();
        $("#login").show();
        $(".collapse").removeClass("show");
    });
     $("#redirect-login").click(function() {
        $("#register").hide();
        $("#login").show();
        $(".collapse").removeClass("show");
    });
     $("#redirect-reg").click(function() {
        $("#login").hide();
        $("#register").show();
        $(".collapse").removeClass("show");
    });
     $(".close-btn").click(function() {
        $("#login").hide();
        $("#register").hide();
    });
        $("#delete-movie-btn").click(function() {
        $("#delete-movie-warn").show();
    });
        $("#cancel-delete-movie").click(function() {
        $("#delete-movie-warn").hide();
    });
        $("#ensure-delete-review").click(function() {
        $("#delete-review-warn").show();
    });
        $("#cancel-delete-review").click(function() {
        $("#delete-review-warn").hide();
    });
        $("#confirm-delete-review").click(function() {
        document.getElementById("delete-review-button").click();
    });
        $(".page-link").click(function() {
        checkEmptyRating();
    });
    
    checkEmptyRating();

    // This part was taken from this w3schools article on how to dynamically display the sliders value https://www.w3schools.com/howto/howto_js_rangeslider.asp
    let slider = document.getElementById("rating");
    let output = document.getElementById("display");
    output.innerHTML = slider.value; 
    slider.oninput = function() {
    output.innerHTML = this.value;
    }
});


function checkEmptyRating() {
    
    // Checks if div contains raiting span and adds text if no raiting exists
    const check = document.getElementsByClassName("rating-wrap");
    for  (let i = 0; i < check.length; i++) {
	 if (check[i].children.length < 2) {
        j = i + 1;
         $("#" + j).html("<p>No Ratings Yet</p>");
         j = 0;
     }
    }
}


