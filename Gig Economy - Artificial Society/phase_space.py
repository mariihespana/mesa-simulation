from mesa.visualization.ModularVisualization import VisualizationElement

class PhaseSpaceModule(VisualizationElement):
    """Scatter plot for hours worked vs earnings."""

    package_includes = ["Chart.min.js"]
    local_includes = ["PhaseSpaceModule.js"]

    def __init__(self, x_label="Horas Trabalhadas", y_label="Ganhos",
                 canvas_width=500, canvas_height=500,
                 data_collector_name="datacollector"):
        self.x_label = x_label
        self.y_label = y_label
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.data_collector_name = data_collector_name

        self.js_code = "new PhaseSpaceModule({}, {}, '{}', '{}', '{}')".format(
            canvas_width,
            canvas_height,
            x_label,
            y_label,
            data_collector_name,
        )
