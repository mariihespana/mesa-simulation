from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random


class DeliveryAgent(Agent):
    """Entregador de aplicativo"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado = "Satisfeito"
        self.hora_entrada = random.randint(10, 20)
        # tempo disponível até 22h
        self.tempo_disponivel_dia = (22 - self.hora_entrada) * 60
        self.meta_diaria = 120  # Gap preenchido: meta_diaria foi fixada em R$120 por simplicidade
        self.renda_minima_por_hora = random.uniform(10, 40)
        self.trabalha_somente_com_app = random.choice([True, False])
        self.faz_pausa_no_cotidiano = random.choice([True, False])
        self.exaustao = 0
        self.reset_daily_vars()

    def reset_daily_vars(self):
        self.renda_dia = 0
        self.horas_trabalhadas_dia = 0
        self.desligou_app = False

    def simulate_day(self):
        tempo_restante = self.tempo_disponivel_dia
        while tempo_restante > 0 and not self.desligou_app:
            valor_pedido = random.uniform(5, 20)
            tempo_entrega = random.randint(20, 60)
            tempo_espera = random.randint(5, 30)
            tempo_total = tempo_entrega + tempo_espera
            renda_por_hora = valor_pedido / (tempo_total / 60)
            if renda_por_hora >= self.renda_minima_por_hora and self.renda_dia < self.meta_diaria:
                self.renda_dia += valor_pedido
                self.horas_trabalhadas_dia += tempo_total
                tempo_restante -= tempo_total
                if self.renda_dia >= self.meta_diaria:
                    self.desligou_app = True
                    self.estado = "Satisfeito"
            else:
                # não aceita o pedido e espera novo
                continue
            if tempo_restante <= 0:
                break
        if self.renda_dia < self.meta_diaria:
            self.desligou_app = True
            self.estado = "Não Satisfeito"
        self.exaustao += self.horas_trabalhadas_dia / 60  # acumula exaustão em horas trabalhadas

    def step(self):
        self.reset_daily_vars()
        self.simulate_day()


def media_renda(model):
    return sum(a.renda_dia for a in model.delivery_agents) / len(model.delivery_agents)


def percent_insatisfeitos(model):
    insatisfeitos = [a for a in model.delivery_agents if a.desligou_app and a.estado == "Não Satisfeito"]
    return len(insatisfeitos) / len(model.delivery_agents)


def exaustao_media(model):
    return sum(a.exaustao for a in model.delivery_agents) / len(model.delivery_agents)


class DeliveryModel(Model):
    def __init__(self, num_agents=10, seed=None):
        super().__init__(seed=seed)
        self.schedule = RandomActivation(self)
        self.delivery_agents = []  # avoid using reserved name `agents` in Mesa 3+
        for i in range(num_agents):
            agent = DeliveryAgent(i, self)
            self.schedule.add(agent)
            self.delivery_agents.append(agent)
        self.datacollector = DataCollector({
            "media_renda": media_renda,
            "percent_insatisfeitos": percent_insatisfeitos,
            "exaustao_media": exaustao_media,
        })

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
