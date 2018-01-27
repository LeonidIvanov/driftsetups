(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

$(document).ready(function(){

    $('.popup-close').click(function() {
            $('.popup-background').css('display', 'none');
            $('.popup-login-content').css('display', 'none');
            $('.popup-sign-up-content').css('display', 'none');
    });

    $('.popup-background').click(function () {
        $('.popup-background').css('display', 'none');
        $('.popup-login-content').css('display', 'none');
        $('.popup-sign-up-content').css('display', 'none');
    });

    $('#login').click(function() {
        $('.popup-background').css('display', 'block');
        $('.popup-login-content').css('display', 'block');
    });


    $('#sign-up').click(function() {
        $('.popup-background').css('display', 'block');
        $('.popup-sign-up-content').css('display', 'block');
    });

    $('.popup-register-close').click(function() {
        $('.popup-background').css('display', 'none');
        $('.popup-register-content').css('display', 'none');
    });
    
    $('.sign-up-with-email').click(function() {
        $('.popup-sign-up-choice').hide();
        $('.sign-up-with-email-form').show();
    })

});