var PhaseSpaceModule = function(width, height, x_label, y_label, dc_name) {
    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height;
    this.dc_name = dc_name;
    var ctx = this.canvas.getContext('2d');
    this.chart = new Chart(ctx, {
        type: 'scatter',
        data: { datasets: [{ label: 'Agentes', data: [] }] },
        options: {
            animation: false,
            scales: {
                x: { title: { display: true, text: x_label } },
                y: { title: { display: true, text: y_label } }
            }
        }
    });
};

PhaseSpaceModule.prototype.render = function(data) {
    var points = data[this.dc_name]['PhaseSpace'];
    this.chart.data.datasets[0].data = points;
    this.chart.update();
};
