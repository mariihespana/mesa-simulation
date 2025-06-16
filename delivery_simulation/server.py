from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import Slider

from model import DeliveryModel, DeliveryAgent

# Portrayal for each agent on a simple grid

def agent_portrayal(agent):
    color = "green" if agent.estado == "Satisfeito" else "red"
    return {"Shape": "circle", "Filled": True, "Layer": 0,
            "Color": color, "r": 0.5}

class DayElement(TextElement):
    def __init__(self):
        super().__init__()
        self.day = 0

    def render(self, model):
        self.day += 1
        return f"Dia: {self.day}"

# grid just for visualization
grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

chart = ChartModule([
    {"Label": "media_renda", "Color": "blue"},
    {"Label": "percent_insatisfeitos", "Color": "red"},
    {"Label": "exaustao_media", "Color": "orange"},
])

model_params = {
    "num_agents": Slider("Número de agentes", 10, 1, 1000, 1),
    "meta_diaria": Slider("Meta diária", 120, 50, 200, 10),
    "renda_min_min": Slider("Renda mínima/hora mínima", 10, 5, 20, 1),
    "renda_min_max": Slider("Renda mínima/hora máxima", 40, 20, 60, 1),
}

server = ModularServer(
    DeliveryModel,
    [grid, DayElement(), chart],
    "Delivery Simulation",
    model_params,
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
