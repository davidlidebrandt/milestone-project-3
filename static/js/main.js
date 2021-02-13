$(document).ready(function () {
    $(".regnav-button").click(function() {
        $("#register").show();
    });
    $(".loginnav-button").click(function() {
        $("#login").show();
    });
     $("#redirect-login").click(function() {
        $("#register").hide();
        $("#login").show();
    });
     $("#redirect-reg").click(function() {
        $("#login").hide();
        $("#register").show();
    });

});