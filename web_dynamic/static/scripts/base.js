$(function () {
  $('.menu-bar').click(function () {
	  const menuHeight = $(this).outerHeight() + 4;
	  const displayStyle = $('nav').css('display');
	  if (displayStyle === 'none') {
		  $('nav').css('display', 'flex');
		  $('nav').css('top', menuHeight);
		  $('nav').addClass('show');
	  } else {
		  $('nav').css('display', 'none');
	  }
  });
  $(document).click(function (event) {
    const nav = $('nav');
    if (!$(event.target).closest('.menu-bar').length && !$(event.target).closest('nav').length) {
      if (nav.css('display') !== 'none') {
        nav.css('display', 'none');
      }
    }
  });
});
