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

    var totalVotes = $('#setup-info-votes-total');
    var voted_up = 0;
    var voted_down = 0;
    $('#vote-up').click(function(e) {
        var totalVotesValue = parseInt($(totalVotes).text());
        var url = $(this).data('vote-up');
        $.get(url, function () {
        });
        if (voted_up == 0 && voted_down == 0) {
            $(totalVotes).text(totalVotesValue + 1);
            voted_up = 1;
        }
    });

    $('#vote-down').click(function(e) {
        var totalVotesValue = parseInt($(totalVotes).text());
        var url = $(this).data('vote-down');
        $.get(url, function() {
        });
        if (voted_down == 0 && voted_up == 0) {
            $(totalVotes).text(totalVotesValue + 1);
            voted_down = 1;
        }
    });

    var setupMainImageHeight = $('.setup-main-image').height();
    console.log(setupMainImageHeight);
    if (setupMainImageHeight > 600) {
        $('.setup-main-image').css('top', (-(setupMainImageHeight - 600)/2))
    };
});

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}

// Get the modal
var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('sliderImage');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
};

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
};

