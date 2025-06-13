from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class DeliveryAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hours_worked = 0
        self.earnings = 0
        self.days_overworked = 0
        self.state = "satisfeito"

    def step(self):
        # Simula trabalho em um dia
        total_hours = 0
        earnings = 0
        while total_hours < self.model.daily_work_limit and earnings < self.model.daily_income_target:
            delivery_time = self.random.randint(*self.model.delivery_time_range)
            delivery_value = self.random.randint(*self.model.delivery_value_range)
            total_hours += delivery_time / 60
            earnings += delivery_value
            if total_hours >= 12:
                break

        self.hours_worked = total_hours
        self.earnings = earnings

        if earnings >= self.model.daily_income_target and total_hours <= 10:
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
    def __init__(self, N=50, daily_income_target=80, daily_work_limit=12, delivery_value_range=(8, 15), delivery_time_range=(30, 60)):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(10, 10, True)
        self.schedule = RandomActivation(self)

        self.daily_income_target = daily_income_target
        self.daily_work_limit = daily_work_limit
        self.delivery_value_range = delivery_value_range
        self.delivery_time_range = delivery_time_range

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
                "Exaustos": lambda m: sum([1 for a in m.schedule.agents if a.state == "exausto"])
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
