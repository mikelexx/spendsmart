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
	    /** 'stroke-dashoffset': circumference**/
	    'stroke-dashoffset': offset

    });

	  /**    $(circle).animate({ 'stroke-dashoffset': offset }, 400); **/
  });

  $(this).find('.category-image').click(function () {
	  console.log('image clicked');
	 $(this).closest('.category-card').find('.analytics-card').css('display', 'flex');
	 $(this).closest('.category-card').find('.analytics-card').css('flex-direction', 'column');
  });
  $(document).on('click', '.close-analytics', function () {
    console.log('close clicked');
    $(this).closest('.category-card').find('.analytics-card').css('display', 'none');
  });
});
