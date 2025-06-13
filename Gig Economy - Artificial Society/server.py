from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from deliveries_model import DeliveryModel, DeliveryAgent

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

chart = ChartModule([
    {"Label": "Satisfeitos", "Color": "green"},
    {"Label": "NaoSatisfeitos", "Color": "orange"},
    {"Label": "Exaustos", "Color": "red"}
])

deliveries_chart = ChartModule(
    [
        {"Label": "Pedidos", "Color": "blue"},
    ])

model_params = {
    "N": 1000,
    "delivery_value_range": (7.5, 10),
    "delivery_time_range": (30, 60),
    "part_time_work_range": (2, 4),
    "full_time_work_range": (6, 12),
    "part_time_income_range": (20, 50),
    "full_time_income_range": (50, 100),
    "wait_time_range": (15, 30),
    "acceptance_rate": 0.8,
}

server = ModularServer(
    DeliveryModel,
    [grid, chart, deliveries_chart],
    "Modelo de Entregadores",
    model_params
)

server.port = 8521
server.running = False  # Encerra se estiver rodando
server.launch()
