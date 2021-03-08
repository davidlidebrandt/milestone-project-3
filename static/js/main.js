localStorage.setItem("user", "");

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
        localStorage.setItem("user", "");
    });

    $("#confirm-delete-review").click(confirmDeleteReview);
    
    $("#confirm-delete-movie").click(confirmDeleteMovie);

    $(".page-link").click(checkEmptyRating);

    setTimeout(function() {
        $(".display-flash").hide()
    }, 5000
    )

    checkEmptyRating();

}); // end of ready function


function checkEmptyRating() {
    /* Checks if div contains rating span and adds text if no rating exists */
    const check = document.getElementsByClassName("rating-wrap");
    for  (let i = 0; i < check.length; i++) {
	 if (check[i].children.length < 2) {
        let j = i + 1;
         $("#" + j).html("<p>No Ratings Yet</p>");
         j = 0;
     }
    }
}

  function deleteReviewWarning() {
        /* Gets the user name for the particular review  and sets the "user" item 
        to that name so that the AJAX call can delete the correct review.*/
        let user = $(this).siblings(".d-none").text();
        localStorage.setItem("user", user);
        $("#delete-review-warn").show();
    }

  function confirmDeleteReview() {
         $.ajax({
              method: "DELETE",
              url: `/deletereview/${$("#title").text()}/${localStorage.getItem("user")}`,
              xhrFields: {withCredentials: true}
          })
             .done(function() {
                 window.location = `/moviepage/${$("#title").text()}`;
                 localStorage.setItem("user", "");
             });
    }

    function confirmDeleteMovie() {
        $.ajax({
            method: "DELETE",
            url: `/moviepage/delete_movie/${$("#title").text()}`,
            xhrFields: {withCredentials: true}
        })
        .done(function() {
            window.location = "/findmovies";
         });
    }

    $("#update-review").submit(function(event) {
        /* Prevent the default action when submitting the form
        and instead let the AJAX call redirect after response*/
    event.preventDefault(); });
   
    function updateReview(form) {
        $.ajax({
            method: "PUT",
            url: `/updatereview/${$("#title").text()}/${form.user.value}`,
            data: JSON.stringify({description: form.review.value}),
            contentType:"application/json; charset=utf-8",
            xhrFields: {withCredentials: true}
        })
        .done(function() {
            window.location = `/moviepage/${$("#title").text()}`;
         });
    }


    $("#update-movie").submit(function(event) {
        /* Prevent the default action when submitting the form
        and instead let the AJAX call redirect after response*/
    event.preventDefault(); });


    function updateMovie(form) {
        $.ajax({
            method: "PUT",
            url: `/updatemovie/${form.id.value}`,
            data: JSON.stringify({title: form.title.value, year: form.year.value, directors: form.directors.value
            , cast: form.cast.value, img_url: form.img_url.value}),
            contentType:"application/json; charset=utf-8",
            xhrFields: {withCredentials: true}
        })
        .done(function() {
            window.location = "/index";
         });
    }

