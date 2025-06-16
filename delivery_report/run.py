from model import DeliveryModel

if __name__ == "__main__":
    model = DeliveryModel(num_agents=50, seed=42)
    for day in range(30):  # simula 30 dias
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    print(data)
    print("Relatório salvo em step_report.csv")
