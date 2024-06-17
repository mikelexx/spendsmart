$(function () {
  console.log('called');
  $('.menu-bar').click(function () {
	  const displayStyle = $('nav').css('display');
	  if (displayStyle === 'none') {
		  $('nav').css('display', 'flex');
		  $('nav').addClass('show');
	  } else {
		  $('nav').css('display', 'none');
	  }
  });
});
