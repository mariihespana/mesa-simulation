var ScatterPlotModule = function(canvas_width, canvas_height) {
    var canvas = document.createElement('canvas');
    canvas.width = canvas_width;
    canvas.height = canvas_height;
    this.canvas = canvas;
    var ctx = canvas.getContext('2d');
    this.chart = new Chart(ctx, {
        type: 'scatter',
        data: { datasets: [{ label: '', data: [] }] },
        options: {
            animation: false,
            scales: {
                x: { type: 'linear', position: 'bottom' },
                y: { beginAtZero: true }
            }
        }
    });
    this.render = function(data) {
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    };
};
