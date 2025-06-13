from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from deliveries_model import DeliveryModel, DeliveryAgent
from visualization import HistogramModule, ScatterPlotModule, StackedAreaChartModule

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": agent.get_color(),
        "Filled": "true",
        "Layer": 0,
        "r": 0.8,
        # Informações exibidas ao clicar no agente
        "Pedidos": agent.deliveries,
        "Renda": round(agent.earnings, 2)
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

states_chart = StackedAreaChartModule([
    {"Label": "Satisfeitos", "Color": "green"},
    {"Label": "NaoSatisfeitos", "Color": "orange"},
    {"Label": "Exaustos", "Color": "red"}
])

deliveries_chart = ChartModule(
    [
        {"Label": "Pedidos", "Color": "blue"},
    ])

hours_hist = HistogramModule(bins=10, calculation=lambda a: a.hours_worked)
earnings_hist = HistogramModule(bins=10, calculation=lambda a: a.earnings)

phase_space = ScatterPlotModule(lambda a: a.hours_worked, lambda a: a.earnings)

model_params = {
    "N": 1000,
    "daily_income_target": 100,
    "daily_work_limit": 12,
    "delivery_value_range": (7.5, 10),
    "delivery_time_range": (30, 60)
}

server = ModularServer(
    DeliveryModel,
    [
        grid,
        states_chart,
        deliveries_chart,
        hours_hist,
        earnings_hist,
        phase_space,
    ],
    "Modelo de Entregadores",
    model_params,
)

server.port = 8521
server.running = False  # Encerra se estiver rodando
server.launch()
