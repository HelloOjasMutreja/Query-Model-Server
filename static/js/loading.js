$(document).ready(function() {
    $('form').submit(function() {
        $('body').addClass('loading');
    });
    $(document).ajaxComplete(function() {
        $('body').removeClass('loading');
    });
});

window.addEventListener("load", function () {
    const loader = document.querySelector(".loader");
    // Add a delay of 5 seconds to simulate a slow-loading page
    setTimeout(function () {
        loader.className += " hidden";
    }, 5000);
});