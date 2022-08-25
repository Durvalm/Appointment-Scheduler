const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        datasets: [{
            label: `Revenue ${new Date().getFullYear()}`,
            data: [1200, 1900, 1350, 1450, 2000, 3000, 3500],
            borderColor: 'rgb(75, 192, 192)' ,  
            fill: false,
            tension: 0.1,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

BASE_URL = 'http://127.0.0.1:8000'
graphDateSelector = document.querySelector('#days-7');
graphDateSelector.addEventListener('click', function(e){
    e.preventDefault()

    $.ajax({
        type: "GET",
        url: `${BASE_URL}/backoffice/filter-graph-seven-days/`,
        data: {
        },
        success: function (data) {
            myChart.data.labels = Object.keys(data)
            myChart.data.datasets[0].data = Object.values(data)
            myChart.update()
        }
    });
    return false;
})
