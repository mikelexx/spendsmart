$(function () {
  $('#mobile-menu').on('click', function () {
    const menuHeight = $(this).outerHeight() + 26; // Calculate menu height including additional 20px
    if ($('.nav-links').css('display') === 'none') {
      $('.nav-links').css({
        display: 'flex',
        'flex-direction': 'column',
        position: 'absolute',
        top: menuHeight + 'px', // Concatenate with 'px' for proper CSS value
        right: '0px',
	 background: 'white'
      });
    } else {
		  $('.nav-links').css('display', 'none');
	  }
  });
});
