$(function() {

    var start = moment().subtract(30, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(7, 'days'), moment()],
           'Last 30 Days': [moment().subtract(30, 'days'), moment()],
           'Last 3 Months': [moment().subtract(90, 'days'), moment()],
           'Last 1 year': [moment().subtract(365, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);
});

BASE_URL = 'http://127.0.0.1:8000'

$('#daterange').daterangepicker();
$('#reportrange').on('hide.daterangepicker', function(ev, picker) {
  startDate = picker.startDate.format('YYYY-MM-DD');
  endDate = picker.endDate.format('YYYY-MM-DD');

  $.ajax({
    type: "GET",
    url: `${BASE_URL}/backoffice/date-filter-dashboard/`,
    data: {
        'startDate': startDate,
        'endDate': endDate,
    },
    success: function (data) {
        document.querySelector('#income').innerHTML = '$'+data.income;
        document.querySelector('#sales').innerHTML = data.sales;
        document.querySelector('#new-customers').innerHTML = data.new_customers;
    }
});
return false;

});
