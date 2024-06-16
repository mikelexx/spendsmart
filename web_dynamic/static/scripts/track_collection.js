$(function () {
  const trackingStartDate = $('#start-date-input');
  const trackingEndDate = $('#end-date-input');

  const f2 = trackingEndDate.flatpickr({
	  	   enableTime: true,
		    dateFormat: 'Y-m-d H:i',
		    defaultDate: 'today',
		    altInput: true,
		    altFormat: 'F j, Y'
  });

  const f1 = trackingStartDate.flatpickr({
    enableTime: true,
    dateFormat: 'Y-m-d H:i:S',
    defaultDate: 'today',
    altInput: true,
    altFormat: 'F j, Y'
  });
  f1.set('onChange', function (selectedDates, dateStr, instance) {
    if (selectedDates.length > 0) {
      const selectedDateTime = selectedDates[0];
      const formattedTime = selectedDateTime.getHours() + ':' + selectedDateTime.getMinutes() + ':00';
      f2.set('minTime', formattedTime);
    }
  });
});
