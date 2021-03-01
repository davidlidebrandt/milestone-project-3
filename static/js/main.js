localStorage.setItem("user", "")

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
    
    $("#ensure-delete-review").click(deleteReviewWarning);
    
    $("#cancel-delete-review").click(function() {
        $("#delete-review-warn").hide();
        localStorage.setItem("user", "")
    });

    $("#confirm-delete-review").click(confirmDeleteReview);
    
    $("#confirm-delete-movie").click(confirmDeleteMovie);

    $(".page-link").click(checkEmptyRating);

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

  function deleteReviewWarning() {
        user = $(this).siblings(".d-none").text()
        localStorage.setItem("user", user)
        $("#delete-review-warn").show();
    }

  function confirmDeleteReview() {
         $.ajax({
              method: "DELETE",
              url: `/deletereview/${$("#title").text()}/${localStorage.getItem("user")}`,
              xhrFields: {withCredentials: true}
          })
             .done(function() {
                 window.location = `/moviepage/${$("#title").text()}`
                 localStorage.setItem("user", "")
             });
    }

    function confirmDeleteMovie() {
           $.ajax({
              method: "DELETE",
              url: `/moviepage/delete_movie/${$("#title").text()}`,
              xhrFields: {withCredentials: true}
          })
             .done(function() {
                 window.location = "/index"
             });
    }
  