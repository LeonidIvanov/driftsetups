// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the navbar
var socialRepost = document.getElementById("social-repost");

// Get the offset position of the navbar
var sticky = socialRepost.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky - 200) {
    socialRepost.classList.add("sticky")
  } else {
    socialRepost.classList.remove("sticky");
  }
}

function showMore(){
	var moretext = "Read full story";
	var lesstext = "Hide";
    if ($('.more p').length > 1) {
        $('.more').each(function() {
            var content = $(this).html();
            var html = content + '<a href="" class="morelink">' + moretext + '</a>';
            $(this).html(html)
        });

        $(".morelink").click(function(){
        if($(this).hasClass("less")) {
			$(this).removeClass("less");
			$(this).html(moretext);
            $('.more p + p').hide();
        } else {
            $('.more p + p').show();
			$(this).addClass("less");
			$(this).html(lesstext);
        }
            return false;
	    });
    }
}



$(document).ready(function(){
    showMore();

    $('#vote-up').click(function(e) {
        console.log('Try up');
        var url = $(this).data('vote-up');
        $.get(url, function() {
        })
    });

    $('#vote-down').click(function(e) {
        console.log('Try down');
        var url = $(this).data('vote-down');
        $.get(url, function() {
        })
    });

    $('#vote-login-up, #vote-login-down').click(function(e) {
        console.log('Login');
    });

});