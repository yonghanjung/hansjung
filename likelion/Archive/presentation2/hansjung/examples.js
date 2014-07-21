$(document).ready(function(){

	$("#demosMenu").change(function(){
		var id = $(this).find("option:selected").attr("id");

		switch (id){
			case 'background':
			window.location.href = 'backgrounds.html';
			break;

			case 'looping':
			window.location.href = 'looping.html';
			break;

			case 'noAnchor':
			window.location.href = 'noAnchor.html';
			break;

			case 'scrollingSpeed':
			window.location.href = 'scrollingSpeed.html';
			break;

			case 'easing':
			window.location.href = 'easing.html';
			break;	

			case 'callbacks':
			window.location.href = 'callback.html';
			break;

			case 'css3':
			window.location.href = 'css3.html';
			break;

			case 'continuous':
			window.location.href = 'continuous.html';

			case 'backgroundVideo':
			window.location.href = 'videoBackground.html';
			break;	 

			case 'normalScroll':
			window.location.href = 'normalScroll.html';
			break;	 	   

			case 'scrolling':
			window.location.href = 'scrolling.html';
			break;	

			case 'navigationV':
			window.location.href = 'navigationV.html';
			break;		      

			case 'navigationH':
			window.location.href = 'navigationH.html';
			break;	

			case 'fixedHeaders':
			window.location.href = 'fixedHeaders.html';
			break;

			case 'gradientBackgrounds':
			window.location.href = 'gradientBackgrounds.html';
			break;	    	

			case 'apple':
			window.location.href = 'apple.html';
			break;	   
		}
	});
/* MY CUSTOMIZE */ 

$("#next").click(function(){
	$(".first").hide()
 	$(".pop1").show()
});

$("#pop1-click").click(function(){
	$(".pop1").hide()
 	$(".second").show()
});

$(".third").click(function(){
	$(".third").hide()
 	$("#imglist").show()
});

$(".pop2-1").click(function(){
	$(".pop2-1").hide()
 	$(".pop2-2").show()
});

$(".pop2-2").click(function(){
	$(".pop2-2").hide()
 	$(".pop2-3").show()
});

$(".pop3-1").click(function(){
	$(".pop3-1").hide()
	$(".pop3-2").show()
});

$(".pop3-2").click(function(){
	$(".pop3-2").hide()
	$(".pop3-3").show()
});

$(".pop4-1").click(function(){
	$(".pop4-1").hide()
	$(".pop4-2").show()
});

$(".pop5-1").click(function(){
	$(".pop5-1").hide()
	$(".pop5-2").show()
});

/* MY Customize done */


});