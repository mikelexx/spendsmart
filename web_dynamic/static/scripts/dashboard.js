$(function () {
  const toast = $('.toast');
  toast.animate({
    top: '70px',
    opacity: 1
  })
    .delay(2500)
    .animate({
      opacity: 0,
      top: '0px'
    }, 400, function () {
      $(this).remove();
    });
  $('div.percentage').each(function () {
	  const percentage = parseFloat($(this).find('.percent').text());
	  const circle = $(this).find('circle')[0];

	  const radius = circle.r.baseVal.value;
	  const circumference = 2 * Math.PI * radius;
	  const offset = circumference - ((percentage / 100) * circumference);
	  /* 0 offset means full circle */
	  $(circle).css({
		  'stroke-dasharray': circumference,
		  'stroke-dashoffset': circumference
	  });

	    $(circle).animate({ 'stroke-dashoffset': offset }, 3000);
  });
});
