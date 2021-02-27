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
        $("#ensure-delete-movie").click(function() {
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
    
      $("#confirm-delete-movie").click(function() {
          console.log(`https://movie-r-and-r.herokuapp.com/moviepage/delete_movie/${$("#title").text()}/`)
        $.ajax({
              method: "DELETE",
              url: `https://movie-r-and-r.herokuapp.com/moviepage/delete_movie/${$("#title").text()}/`
          })
              .done(function () {
                  alert("Success");
              });
      });

        $(".page-link").click(function() {
        checkEmptyRating();
    });
    
    checkEmptyRating();

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


