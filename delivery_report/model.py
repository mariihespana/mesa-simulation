from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import csv
import random


class DeliveryAgent(Agent):
    """Entregador de aplicativo"""

    def __init__(self, unique_id, model, meta_diaria, renda_min_min, renda_min_max):
        super().__init__(unique_id, model)
        self.estado = "Satisfeito"
        self.hora_entrada = random.randint(10, 20)
        # tempo disponível até 22h
        self.tempo_disponivel_dia = (22 - self.hora_entrada) * 60
        self.meta_diaria = meta_diaria  # Gap preenchido: meta_diaria padronizada
        self.renda_minima_por_hora = random.uniform(renda_min_min, renda_min_max)
        self.trabalha_somente_com_app = random.choice([True, False])
        self.faz_pausa_no_cotidiano = random.choice([True, False])
        # self.exaustao = 0
        self.reset_daily_vars()

    def reset_daily_vars(self):
        self.renda_dia = 0
        self.horas_trabalhadas_dia = 0
        self.desligou_app = False
        self.historico_pedidos = []

    def simulate_day(self):
        tempo_restante = self.tempo_disponivel_dia
        tempo_acumulado = 0
        while tempo_restante > 0 and not self.desligou_app:
            valor_pedido = random.uniform(
                self.model.valor_pedido_min, self.model.valor_pedido_max
            )
            tempo_entrega = random.randint(20, 60)
            tempo_espera = random.randint(5, 30)
            tempo_total = tempo_entrega + tempo_espera
            renda_por_hora = valor_pedido / (tempo_total / 60)
            aceita = False
            limite = self.renda_minima_por_hora * (
                1 + self.model.tolerancia_percentual / 100
            )
            if renda_por_hora >= limite and self.renda_dia < self.meta_diaria:
                aceita = True
                self.renda_dia += valor_pedido
                self.horas_trabalhadas_dia += tempo_total
                tempo_acumulado += tempo_total
                tempo_restante -= tempo_total
                if self.renda_dia >= self.meta_diaria:
                    self.desligou_app = True
                    self.estado = "Satisfeito"
            else:
                # rejeita o pedido, mas contabiliza o tempo de espera
                self.horas_trabalhadas_dia += tempo_espera
                tempo_acumulado += tempo_espera
                tempo_restante -= tempo_espera
            self.historico_pedidos.append({
                "valor_pedido": round(valor_pedido, 2),
                "tempo_entrega": tempo_entrega,
                "tempo_espera": tempo_espera,
                "tempo_total": tempo_total,
                "renda_por_hora": round(renda_por_hora, 2),
                "aceitou": aceita,
                "tempo_acumulado": tempo_acumulado,
                "desligou_app": self.desligou_app,
            })
            if tempo_restante <= 0:
                break
        if self.renda_dia < self.meta_diaria:
            self.desligou_app = True
            self.estado = "Não Satisfeito"
            if self.historico_pedidos:
                self.historico_pedidos[-1]["desligou_app"] = True
        # self.exaustao += self.horas_trabalhadas_dia / 60  # acumula exaustão em horas trabalhadas

    def step(self):
        self.reset_daily_vars()
        self.simulate_day()


def media_renda(model):
    return sum(a.renda_dia for a in model.delivery_agents) / len(model.delivery_agents)


def renda_media_satisfeitos(model):
    satis = [a for a in model.delivery_agents if a.estado == "Satisfeito"]
    if satis:
        return sum(a.renda_dia for a in satis) / len(satis)
    return 0


def renda_media_insatisfeitos(model):
    insatis = [a for a in model.delivery_agents if a.estado == "Não Satisfeito"]
    if insatis:
        return sum(a.renda_dia for a in insatis) / len(insatis)
    return 0


def percent_insatisfeitos(model):
    insatisfeitos = [a for a in model.delivery_agents if a.desligou_app and a.estado == "Não Satisfeito"]
    return len(insatisfeitos) / len(model.delivery_agents)


def percent_satisfeitos(model):
    satisfeitos = [a for a in model.delivery_agents if a.estado == "Satisfeito"]
    return len(satisfeitos) / len(model.delivery_agents)


# def exaustao_media(model):
#     return sum(a.exaustao for a in model.delivery_agents) / len(model.delivery_agents)


class DeliveryModel(Model):
    def __init__(
        self,
        num_agents=10,
        meta_diaria=120,
        renda_min_min=10,
        renda_min_max=40,
        valor_pedido_min=5,
        valor_pedido_max=20,
        tolerancia_percentual=0,
        seed=None,
    ):
        super().__init__(seed=seed)
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(10, 10, torus=False)
        self.tolerancia_percentual = tolerancia_percentual
        self.valor_pedido_min = valor_pedido_min
        self.valor_pedido_max = valor_pedido_max
        self.delivery_agents = []  # avoid using reserved name `agents` in Mesa 3+
        for i in range(num_agents):
            agent = DeliveryAgent(i, self, meta_diaria, renda_min_min, renda_min_max)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.delivery_agents.append(agent)
        self.datacollector = DataCollector({
            "renda_media_satisfeitos": renda_media_satisfeitos,
            "renda_media_insatisfeitos": renda_media_insatisfeitos,
            "percent_satisfeitos": percent_satisfeitos,
            "percent_insatisfeitos": percent_insatisfeitos,
        })
        self.current_step = 0

    def step(self):
        self.current_step += 1
        self.schedule.step()
        self._save_step_report()
        self.datacollector.collect(self)

    def _save_step_report(self):
        """Append order data for the current step to CSV."""
        filename = "step_report.csv"
        write_header = False
        try:
            with open(filename, "r"):
                pass
        except FileNotFoundError:
            write_header = True
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow([
                    "step",
                    "agent_id",
                    "estado",
                    "meta_diaria",
                    "renda_minima_por_hora",
                    "valor_pedido",
                    "tempo_entrega",
                    "tempo_espera",
                    "tempo_total",
                    "renda_por_hora",
                    "aceitou",
                    "tempo_acumulado",
                    "desligou_app",
                ])
            for ag in self.delivery_agents:
                for pedido in ag.historico_pedidos:
                    writer.writerow([
                        self.current_step,
                        ag.unique_id,
                        ag.estado,
                        ag.meta_diaria,
                        round(ag.renda_minima_por_hora, 2),
                        pedido["valor_pedido"],
                        pedido["tempo_entrega"],
                        pedido["tempo_espera"],
                        pedido["tempo_total"],
                        pedido["renda_por_hora"],
                        pedido["aceitou"],
                        pedido["tempo_acumulado"],
                        pedido["desligou_app"],
                    ])



