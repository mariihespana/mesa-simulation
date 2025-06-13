from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def _compute_hist(data, bins=10):
    """Return a histogram count list for the given data."""
    if not data:
        return [0] * bins
    min_val = min(data)
    max_val = max(data)
    if max_val == min_val:
        hist = [0] * bins
        hist[0] = len(data)
        return hist
    bin_size = (max_val - min_val) / bins
    hist = [0] * bins
    for value in data:
        index = int((value - min_val) / bin_size)
        if index >= bins:
            index = bins - 1
        hist[index] += 1
    return hist


class DeliveryAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hours_worked = 0
        self.earnings = 0
        self.deliveries = 0
        self.days_overworked = 0
        self.state = "satisfeito"

        # Define se o entregador trabalha meio período ou período integral
        if self.random.random() < 0.5:
            self.work_type = "part_time"
            self.daily_work_limit = self.random.uniform(
                *self.model.part_time_work_range
            )
            self.daily_income_target = self.random.uniform(
                *self.model.part_time_income_range
            )
        else:
            self.work_type = "full_time"
            self.daily_work_limit = self.random.uniform(
                *self.model.full_time_work_range
            )
            self.daily_income_target = self.random.uniform(
                *self.model.full_time_income_range
            )

    def step(self):
        """Simula um dia de trabalho do entregador."""
        total_hours = 0
        earnings = 0
        deliveries = 0

        # Continua trabalhando enquanto houver horas disponíveis e não atingir a meta
        while total_hours < self.daily_work_limit and earnings < self.daily_income_target:
            # Tempo de espera até a próxima entrega
            wait_time = self.random.uniform(*self.model.wait_time_range)
            total_hours += wait_time / 60
            self.model.wait_times.append(wait_time)
            if total_hours >= self.daily_work_limit:
                break

            # Decide se aceita a entrega
            if self.random.random() < self.model.acceptance_rate:
                delivery_time = self.random.randint(*self.model.delivery_time_range)
                delivery_value = self.random.uniform(*self.model.delivery_value_range)
                total_hours += delivery_time / 60
                earnings += delivery_value
                deliveries += 1
                self.model.delivery_values.append(delivery_value)
            # Se não aceitar, volta para o loop e espera a próxima

        self.hours_worked = total_hours
        self.earnings = earnings
        self.deliveries = deliveries

        if earnings >= self.daily_income_target and total_hours <= 10:
            self.state = "satisfeito"
            self.days_overworked = 0
        elif total_hours > 10:
            self.days_overworked += 1
            if self.days_overworked >= 3:
                self.state = "exausto"
            else:
                self.state = "não satisfeito"
        else:
            self.state = "não satisfeito"

    def get_color(self):
        return {
            "satisfeito": "green",
            "não satisfeito": "orange",
            "exausto": "red"
        }[self.state]


class DeliveryModel(Model):
    def __init__(
        self,
        N=50,
        daily_income_target=80,
        daily_work_limit=12,
        delivery_value_range=(8, 15),
        delivery_time_range=(30, 60),
        part_time_work_range=(2, 4),
        full_time_work_range=(6, 12),
        part_time_income_range=(20, 50),
        full_time_income_range=(50, 100),
        wait_time_range=(15, 30),
        acceptance_rate=0.8,
    ):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(50, 50, True)
        self.schedule = RandomActivation(self)

        self.daily_income_target = daily_income_target
        self.daily_work_limit = daily_work_limit
        self.delivery_value_range = delivery_value_range
        self.delivery_time_range = delivery_time_range
        self.part_time_work_range = part_time_work_range
        self.full_time_work_range = full_time_work_range
        self.part_time_income_range = part_time_income_range
        self.full_time_income_range = full_time_income_range
        self.wait_time_range = wait_time_range
        self.acceptance_rate = acceptance_rate

        # Lists to store values for histograms each step
        self.delivery_values = []
        self.wait_times = []

        for i in range(self.num_agents):
            a = DeliveryAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={
                "Satisfeitos": lambda m: sum([1 for a in m.schedule.agents if a.state == "satisfeito"]),
                "NaoSatisfeitos": lambda m: sum([1 for a in m.schedule.agents if a.state == "não satisfeito"]),
                "Exaustos": lambda m: sum([1 for a in m.schedule.agents if a.state == "exausto"]),
                "Pedidos": lambda m: sum(a.deliveries for a in m.schedule.agents),
                **{f"ValueBin{i}": (lambda i: lambda m: _compute_hist(m.delivery_values)[i])(i) for i in range(10)},
                **{f"WaitBin{i}": (lambda i: lambda m: _compute_hist(m.wait_times)[i])(i) for i in range(10)},
            }
        )

    def step(self):
        # Reset per-step logs
        self.delivery_values.clear()
        self.wait_times.clear()
        self.schedule.step()
        self.datacollector.collect(self)
