from model import DeliveryModel
import csv

if __name__ == "__main__":
    model = DeliveryModel(num_agents=50, seed=42)
    with open("initial_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "estado",
            "hora_entrada",
            "tempo_disponivel_dia",
            "meta_diaria",
            "renda_minima_por_hora",
            "trabalha_somente_com_app",
            "faz_pausa_no_cotidiano",
        ])
        for ag in model.delivery_agents:
            writer.writerow([
                ag.unique_id,
                ag.estado,
                ag.hora_entrada,
                ag.tempo_disponivel_dia,
                ag.meta_diaria,
                round(ag.renda_minima_por_hora, 2),
                ag.trabalha_somente_com_app,
                ag.faz_pausa_no_cotidiano,
            ])
    print("Relatório salvo em initial_report.csv")
