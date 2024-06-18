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

  const trackingStartDate = $('#start-date-input');
  const trackingEndDate = $('#end-date-input');

  const f2 = trackingEndDate.flatpickr({
	  		position: 'above auto',
	  	   enableTime: true,
		    dateFormat: 'Y-m-d H:i:S',
		    defaultDate: 'today',
		    altInput: true,
		    altFormat: 'F j, Y  G:i K'
  });

  const f1 = trackingStartDate.flatpickr({
	  position: 'above auto',
    enableTime: true,
    dateFormat: 'Y-m-d H:i:S',
    defaultDate: 'today',
    altInput: true,
	  altFormat: 'F j, Y  G:i K'
  });
  $('#description-toggle').change(function () {
    if ($(this).is(':checked')) {
      $('#description-group').slideDown();
    } else {
      $('#description-group').slideUp();
    }
  });
});
