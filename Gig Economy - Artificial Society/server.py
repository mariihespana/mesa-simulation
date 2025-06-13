from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from deliveries_model import DeliveryModel, DeliveryAgent

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": agent.get_color(),
        "Filled": "true",
        "Layer": 0,
        "r": 0.8
    }
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule([
    {"Label": "Satisfeitos", "Color": "green"},
    {"Label": "NaoSatisfeitos", "Color": "orange"},
    {"Label": "Exaustos", "Color": "red"}
])

model_params = {
    "N": 50,
    "daily_income_target": 100,
    "daily_work_limit": 8,
    "delivery_value_range": (8, 15),
    "delivery_time_range": (30, 60),
}

server = ModularServer(
    DeliveryModel,
    [grid, chart],
    "Modelo de Entregadores",
    model_params
)

server.port = 8521
server.running = False  # stop previous server if running
server.launch()
