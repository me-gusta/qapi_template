$(document).ready(function () {
	$(".back2Top").click(function(event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, "slow");
		$('#stickThis').height("auto");
		$('body').removeClass('stick');
        return false;
    });
	$("#menuToggle").click(function(event) {
        $("body").toggleClass("sidebarToggle");
		$("body").removeClass("showMobileMenu");
    });	
	$("#mobileMenuToggle").click(function(event) {
        $("body").toggleClass("showMobileMenu");
		$("body").removeClass("sidebarToggle");
    });	
	
	
});

function sticktothebottom() {
    var h = window.innerHeight;
    var window_top = $(window).scrollTop();
    var top = $('#stick-here').offset().top;
    var panelh = $("#stickThis").height();
    if (window_top + h > top) {
		$('#stickThis').height($('#stickThis').height());
        $('body').addClass('stick');
    } else {
		$('#stickThis').height("auto");
		$('body').removeClass('stick');
	}
}
$(function() {
    $(window).scroll(sticktothebottom);
    sticktothebottom();
});