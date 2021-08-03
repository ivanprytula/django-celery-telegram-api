
$(function ($) {
    let url = window.location.href;
    $('li a').each(function () {
        if (this.href === url) {
            $(this).addClass('active');
        }
    });
});