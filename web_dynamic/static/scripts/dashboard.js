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
});
