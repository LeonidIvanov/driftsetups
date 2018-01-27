function facebookShare(){

    var getWindowOptions = function() {
        var width = 500;
        var height = 450;
        var left = (window.innerWidth / 2) - (width / 2);
        var top = (window.innerHeight / 2) - (height / 2);

        return [
        'resizable,scrollbars,status',
        'height=' + height,
        'width=' + width,
        'left=' + left,
        'top=' + top,
        ].join();
    };
    var fbBtn = document.querySelector('.facebook');
    var title = encodeURIComponent('Hey everyone, come & see how good I look!');
    var shareUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + location.href + '&title=' + title;
    fbBtn.href = shareUrl; // 1

    fbBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var win = window.open(shareUrl, 'ShareOnFb', getWindowOptions());
      win.opener = null; // 2
    });


}


$(document).ready(function(){

    facebookShare();

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