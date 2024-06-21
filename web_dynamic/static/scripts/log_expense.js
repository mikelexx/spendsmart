$(function () {
  const toast = $('.toast');
  toast.animate({
    top: '60px',
    opacity: 1
  }, 300)
    .delay(2500)
    .animate({
      opacity: 0,
      top: '0px'
    }, 400, function () {
      $(this).remove();
    });

  const purchase_date = $('#purchase-date-input');
  purchase_date.flatpickr({
    position: 'above auto',
	  	   enableTime: true,
		    dateFormat: 'Y-m-d H:i:S',
		    defaultDate: new Date(),
		    altInput: true,
		    altFormat: 'F j, Y  G:i K'
  });
});
