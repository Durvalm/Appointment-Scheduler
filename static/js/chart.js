const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday'],
        datasets: [{
            label: 'Revenue',
            data: [1200, 1900, 1350, 1450, 2000, 3000, 3500],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)'
                
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)'   
            ],
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

