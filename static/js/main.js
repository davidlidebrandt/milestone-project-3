$(document).ready(function () {
    $(".regnav-button").click(function() {
        $("#login").hide();
        $("#register").show();
        $(".collapse").removeClass("show");
    });
    $(".loginnav-button").click(function() {
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

});

function checkEmptyRating() {
  
    const check = document.querySelectorAll(".rating-wrap");
    for (let i = 0; i < check.length; i++) {
    console.log(check[i])
	 if (check[i].children.length < 2) {
         let j = i + 1;
         $("#" + j).html("No Ratings Yet");
         j = 0;
     }
	}
    
}

checkEmptyRating();
