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

  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 7);
  const trackingStartDate = $('#start-date-input');
  const trackingEndDate = $('#end-date-input');

  trackingEndDate.flatpickr({
    position: 'above auto',
    enableTime: true,
    dateFormat: 'Z',
    defaultDate: tomorrow,
    altInput: true,
    altFormat: 'F j, Y  G:i K',
    minuteIncrement: 1
  });

  trackingStartDate.flatpickr({
    position: 'above auto',
    enableTime: true,
    dateFormat: 'Z',
    defaultDate: new Date(),
    altInput: true,
    altFormat: 'F j, Y  G:i K',
    minuteIncrement: 1
  });
  $('#description-toggle').change(function () {
    if ($(this).is(':checked')) {
      $('#description-group').slideDown();
    } else {
      $('#description-group').slideUp();
    }
  });
});
