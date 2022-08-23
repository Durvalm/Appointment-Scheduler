const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday'],
        datasets: [{
            label: 'Revenue',
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

document.querySelector('#overview').addEventListener('click', function(){
    console.log(myChart.data.labels);
    myChart.data.labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    myChart.update()
})

