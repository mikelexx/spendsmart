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

    // Handle cases where percentage exceeds 100%
    const adjustedPercentage = Math.min(percentage, 100);
    const offset = circumference - ((adjustedPercentage / 100) * circumference);

    $(circle).css({
      'stroke-dasharray': circumference,
      'stroke-dashoffset': offset
    });

    // Change the stroke color for percentages over 100%
    if (percentage >= 100) {
      $(circle).css('stroke', '#FF0000'); // Red color for over 100%
    }
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

  $('#select-all').on('click', function () {
    $('.expense-checkbox').each(function () {
      this.checked = !this.checked;
    });
  });
  function validateCheckboxSelection () {
    const selectedInputsCount = $('input[name="expense_ids"]:checked').length;
    if (selectedInputsCount === 0) {
      alert('Please select at least one expense to proceed.');
      return false;
    }
    return true;
  }

  $('#expenses-form').submit(function (event) {
    if (!validateCheckboxSelection()) {
      event.preventDefault();
    }
  });

  $('#move-to-selector').change(function () {
    if (validateCheckboxSelection()) {
      $('#expenses-form').submit();
    }
  });
  $('#move-to').click(function () {
    const selector = $('#move-to-selector');
    if (selector.css('display') === 'none') {
      selector.css('display', 'inline-block');
      selector.prop('selectedIndex', -1);
      selector.attr('size', selector.children('option').length);
    } else {
      selector.css('display', 'none');
    }
  });
  $(document).click(function (event) {
    const selector = $('#move-to-selector');
    if (!$(event.target).closest('#move-to').length && !$(event.target).closest('#move-to-selector').length) {
      if (selector.css('display') !== 'none') {
        selector.css('display', 'none');
      }
    }
  });
});
