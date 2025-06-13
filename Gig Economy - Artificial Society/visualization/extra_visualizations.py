from mesa.visualization.ModularVisualization import VisualizationElement

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins=10, canvas_height=200, canvas_width=500, calculation=None):
        """Create a new HistogramModule.

        Args:
            bins: Number of bins to divide data into.
            canvas_height: Height of the canvas in pixels.
            canvas_width: Width of the canvas in pixels.
            calculation: Function that receives an agent and returns the value
                to be aggregated. If None, the agent itself will be used.
        """
        self.bins = bins
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.calculation = calculation or (lambda a: a)
        new_element = f"new HistogramModule({bins}, {canvas_width}, {canvas_height})"
        super().__init__(new_element)

    def render(self, model):
        values = [self.calculation(agent) for agent in model.schedule.agents]
        if not values:
            return [0 for _ in range(self.bins)]
        min_val = min(values)
        max_val = max(values)
        if min_val == max_val:
            counts = [0] * self.bins
            counts[0] = len(values)
            return counts
        bin_width = (max_val - min_val) / float(self.bins)
        counts = [0] * self.bins
        for v in values:
            idx = int((v - min_val) / bin_width)
            if idx >= self.bins:
                idx = self.bins - 1
            counts[idx] += 1
        return counts


class ScatterPlotModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["ScatterPlotModule.js"]

    def __init__(self, x_fn, y_fn, canvas_height=200, canvas_width=500):
        """Create a new ScatterPlotModule.

        Args:
            x_fn: Function that extracts the x value from an agent.
            y_fn: Function that extracts the y value from an agent.
        """
        self.x_fn = x_fn
        self.y_fn = y_fn
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = f"new ScatterPlotModule({canvas_width}, {canvas_height})"
        super().__init__(new_element)

    def render(self, model):
        data = []
        for agent in model.schedule.agents:
            data.append({"x": self.x_fn(agent), "y": self.y_fn(agent)})
        return data


class StackedAreaChartModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["StackedAreaChartModule.js"]

    def __init__(self, series, canvas_height=200, canvas_width=500, data_collector_name="datacollector"):
        """Create a stacked area chart module.

        Args:
            series: List of dictionaries with "Label" and "Color" keys.
            canvas_height: Canvas height.
            canvas_width: Canvas width.
            data_collector_name: Name of the model's DataCollector.
        """
        self.series = series
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data_collector_name = data_collector_name
        new_element = (
            f"new StackedAreaChartModule({series}, {canvas_width}, {canvas_height})"
        )
        super().__init__(new_element)

    def render(self, model):
        dc = getattr(model, self.data_collector_name)
        model_vars = dc.get_model_vars_dataframe()
        latest = model_vars.iloc[-1]
        return latest.to_dict()
