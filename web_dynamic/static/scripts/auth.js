$(function(){
	const toast = $('.toast');
	toast.animate({
		top: '60px',
		opacity: 1
	})
	.delay(1500)
	.animate({
		opacity:0,
		top: '0px'
	}, 400, function(){
		$(this).remove();
	});

});
