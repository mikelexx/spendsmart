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

  const purchaseDate = $('#purchase-date-input');
  purchaseDate.flatpickr({
    position: 'above auto',
    enableTime: true,
    dateFormat: 'Z',
    defaultDate: new Date(),
    altInput: true,
    altFormat: 'F j, Y  G:i K'
  });
});
