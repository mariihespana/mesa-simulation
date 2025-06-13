var HistogramModule = function(bins, canvas_width, canvas_height) {
    var canvas = document.createElement('canvas');
    canvas.width = canvas_width;
    canvas.height = canvas_height;
    this.canvas = canvas;
    var ctx = canvas.getContext('2d');
    var labels = [];
    for (var i = 0; i < bins; i++) {
        labels.push(i.toString());
    }
    this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: new Array(bins).fill(0)
            }]
        },
        options: {
            animation: false,
            scales: { y: { beginAtZero: true } }
        }
    });
    this.render = function(data) {
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    };
};
