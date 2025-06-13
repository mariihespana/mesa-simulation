var StackedAreaChartModule = function(series, canvas_width, canvas_height) {
    var canvas = document.createElement('canvas');
    canvas.width = canvas_width;
    canvas.height = canvas_height;
    this.canvas = canvas;
    var ctx = canvas.getContext('2d');
    var datasets = [];
    for (var i = 0; i < series.length; i++) {
        datasets.push({
            label: series[i].Label,
            borderColor: series[i].Color,
            backgroundColor: series[i].Color,
            fill: true,
            data: []
        });
    }
    this.chart = new Chart(ctx, {
        type: 'line',
        data: { labels: [], datasets: datasets },
        options: {
            animation: false,
            scales: {
                x: { stacked: true },
                y: { stacked: true, beginAtZero: true }
            }
        }
    });
    this.step = 0;
    this.render = function(data) {
        this.chart.data.labels.push(this.step.toString());
        this.step += 1;
        for (var i = 0; i < datasets.length; i++) {
            var label = series[i].Label;
            this.chart.data.datasets[i].data.push(data[label]);
        }
        this.chart.update();
    };
};
