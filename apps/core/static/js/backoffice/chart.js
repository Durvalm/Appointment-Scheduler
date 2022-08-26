
BASE_URL = 'http://127.0.0.1:8000'

// Get data from the backend to display dynamically in the chart
const updateChart = async function(dateRange) {
    const res = await fetch(`${BASE_URL}/backoffice/${dateRange}/`)
    const data = await res.json()
    return data
}

// For each date range, get data from the back and display it by replacing values in the Chart canvas
graphRange = document.querySelectorAll('#graph-range span');
graphRange.forEach(dateRange => {
    dateRange.addEventListener('click', function(e){
        e.preventDefault();

        updateChart(dateRange.id).then((data) => {
            console.log(data);
            myChart.data.labels = Object.keys(data)
            myChart.data.datasets[0].data = Object.values(data)
            myChart.update()
        })
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
