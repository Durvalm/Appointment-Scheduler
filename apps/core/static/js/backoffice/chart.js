
BASE_URL = 'http://127.0.0.1:8000'

// For each date range, get data from the back and display it by replacing values in the Chart canvas
graphRange = document.querySelectorAll('#graph-range span');
graphRange.forEach(dateRange => {
    dateRange.addEventListener('click', function(e){
        e.preventDefault();

        $.ajax({
            type: "GET",
            url: `${BASE_URL}/backoffice/date-filter-graph/`,
            data: {
                days: dateRange.id
            },
            success: function (data) {
                myChart.data.labels = Object.keys(data)
                myChart.data.datasets[0].data = Object.values(data)
                myChart.update()
            }
        });
        return false;
    })
});

// Convert html content into array to display days in graph
graphMonthHTML = [...document.querySelectorAll('#graph_months')];
graphMonths = []
graphMonthHTML.forEach(month => {
    graphMonths.push(month.textContent)
});

// Chart configuration
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx,{
    type: 'line',
    data: {
        labels: graphMonths,
        datasets: [{
            label: `Revenue`,
            data: graphSales,
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
