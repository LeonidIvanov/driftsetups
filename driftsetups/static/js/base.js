function socialShare(){

    var getWindowOptions = function() {
        var width = 575;
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

    var title = $("meta[property='og:title']").attr('content');
    var description = $("meta[property='og:description']").attr('content');
    var img = $("meta[property='og:img']").attr('content');


    var fbShareUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + location.href + '&title=' + title + '&description=' + description + '&img=' + img;
    var twShareUrl = 'https://twitter.com/intent/tweet?url=' + location.href + '&text=' + title + '&hashtags=DRIFTSETUPS';
    var vkShareUrl = 'https://vk.com/share.php?url=' + location.href + '&title=' + title + '&description=' + description + '&img=' + img;

    var fbBtn = document.querySelector('.facebook');
    var twBtn = document.querySelector('.twitter');
    var vkBtn = document.querySelector('.vkontakte');

    fbBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var win = window.open(fbShareUrl, 'shareOnFacebook', getWindowOptions());
      win.opener = null;
    });

    twBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var win = window.open(twShareUrl, 'shareOnTwitter', getWindowOptions());
      win.opener = null;
    });

    vkBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var win = window.open(vkShareUrl, 'shareOnVkontakte', getWindowOptions());
      win.opener = null;
    });
}


$(document).ready(function(){

    socialShare();

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