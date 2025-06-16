from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import Slider

from model import DeliveryModel, DeliveryAgent

# Portrayal for each agent on a simple grid

def agent_portrayal(agent):
    color = "green" if agent.estado == "Satisfeito" else "red"
    progresso = 0
    if agent.meta_diaria > 0:
        progresso = agent.renda_dia / agent.meta_diaria
    label = f"{agent.estado}\n{agent.horas_trabalhadas_dia} min\n{progresso:.0%}"
    return {
        "Shape": "circle",
        "Filled": True,
        "Layer": 0,
        "Color": color,
        "r": 0.5,
        "text": label,
        "text_color": "black",
    }

class DayElement(TextElement):
    def __init__(self):
        super().__init__()
        self.day = 0

    def render(self, model):
        self.day += 1
        return f"Dia: {self.day}"

# grid just for visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

income_chart = ChartModule([
    {"Label": "renda_media_satisfeitos", "Color": "green"},
    {"Label": "renda_media_insatisfeitos", "Color": "red"},
])

satisfaction_chart = ChartModule([
    {"Label": "percent_satisfeitos", "Color": "green"},
    {"Label": "percent_insatisfeitos", "Color": "red"},
])

model_params = {
    "num_agents": Slider("Número de agentes", 10, 1, 100, 1),
    "meta_diaria": Slider("Meta diária", 120, 50, 200, 10),
    "tolerancia_percentual": Slider(
        "Tolerância rejeição (%)", 0, -20, 0, 1,
        description="Aceita pedidos até essa porcentagem abaixo da renda mínima"
    ),
}

server = ModularServer(
    DeliveryModel,
    [grid, DayElement(), income_chart, satisfaction_chart],
    "Delivery Simulation",
    model_params,
)

if __name__ == "__main__":
    server.port = 8522
    server.launch()
