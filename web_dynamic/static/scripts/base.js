$(function () {
  $('.menu-bar').click(function (event) {
    event.stopPropagation(); // Prevent the click event from propagating to the document
    const menuHeight = $(this).outerHeight() + 4;
    const displayStyle = $('nav').css('display');
    if (displayStyle === 'none') {
      $('nav').css('display', 'flex');
      $('nav').css('top', menuHeight);
      $('nav').addClass('show');
    } else {
      $('nav').css('display', 'none');
      $('nav').removeClass('show');
    }
  });
});
