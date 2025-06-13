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

chart = ChartModule(
    [
        {"Label": "Satisfeitos", "Color": "green"},
        {"Label": "NaoSatisfeitos", "Color": "orange"},
        {"Label": "Exaustos", "Color": "red"},
    ],
    data_collector_name="datacollector",
    chart_type="line",
    title="Estados dos Entregadores",
    x_label="Ticks",
    y_label="Agentes",
)

hours_chart = ChartModule(
    [
        {"Label": "HorasTrabalhadas", "Color": "blue"},
    ],
    data_collector_name="datacollector",
    chart_type="scatter",
    title="Horas Trabalhadas por Tick",
    x_label="Ticks",
    y_label="Horas",
)

model_params = {
    "N": 1000,
    "daily_income_target": 100,
    "daily_work_limit": 12,
    "delivery_value_range": (7.5, 10),
    "delivery_time_range": (30, 60)
}

server = ModularServer(
    DeliveryModel,
    [grid, chart, hours_chart],
    "Modelo de Entregadores",
    model_params
)

server.port = 8521
server.running = False  # Encerra se estiver rodando
server.launch()
