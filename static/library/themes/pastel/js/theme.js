;(function($){
    "use strict"


    var nav_offset_top = $('header').height() + 50; 
    /*-------------------------------------------------------------------------------
	  Navbar 
     -------------------------------------------------------------------------------*/

	//* Navbar Fixed  
    function navbarFixed(){
        if ( $('.header_area').length ){ 
            $(window).scroll(function() {
                var scroll = $(window).scrollTop();   
                if (scroll >= nav_offset_top ) {
                    $(".header_area").addClass("navbar_fixed");
                } else {
                    $(".header_area").removeClass("navbar_fixed");
                }
            });
        };
    };
    navbarFixed();





    /*----------------------------------------------------*/
    /*  Parallax Effect js
    /*----------------------------------------------------*/
    function parallaxEffect() {
    	$('.bg-parallax').parallax();
    }
    parallaxEffect();

    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });


      //------- Owl Carusel  js --------//





      $(document).ready(function() {

    $(".banner-area").owlCarousel({
        items: 1,
        autoplay: 2500,
        autoplayTimeout: 5000,
        loop: true,
        nav: true,
        dots: false,
        navText : ['<img src="img/elements/arrow.png" alt="">','<img src="img/elements/arrow.png" alt="">']
    });

    $('.testimonial').owlCarousel({
        items: 2,
        loop: true,
        margin: 30,
        autoplayHoverPause: true,
        smartSpeed:500,
        dots: false,
        responsive: {
            768: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });


    $('.play-video').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });



});




 //------- mailchimp --------//  
 function mailChimp() {
    $('#mc_embed_signup').find('form').ajaxChimp();
}
mailChimp();







})(jQuery)