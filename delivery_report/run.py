from model import DeliveryModel

if __name__ == "__main__":
    # exemplo de tolerância de -5% e valor de pedidos entre 5 e 20
    model = DeliveryModel(
        num_agents=50,
        tolerancia_percentual=-5,
        valor_pedido_min=5,
        valor_pedido_max=20,
        seed=42,
    )
    for day in range(30):  # simula 30 dias
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    print(data)
    print("Relatório salvo em step_report.csv")
