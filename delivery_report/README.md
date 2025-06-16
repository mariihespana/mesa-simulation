# Delivery Simulation

Este diretório contém uma simulação simples de entregadores por aplicativo utilizando o framework Mesa. A implementação segue o enunciado fornecido e preenche algumas lacunas com suposições descritas no código.

## Requisitos

- Python 3.11+
- Mesa (veja `requirements.txt`)

## Execução

```bash
pip install -r requirements.txt
python run.py            # executa simulação de forma simples
python server.py         # abre interface interativa no navegador
```

O script `run.py` executa a simulação por 30 dias para 50 agentes e imprime as estatísticas coletadas. O `server.py` inicia uma interface web com sliders para acompanhar a execução. O `report.py` gera um CSV (`initial_report.csv`) com as variáveis iniciais de cada agente.
Além disso, a cada passo de simulação é criado o arquivo `step_report.csv` contendo o histórico de pedidos aceitos ou rejeitados por cada agente e os tempos envolvidos.
O slider **Tolerância rejeição (%)** permite ajustar o quanto abaixo da renda mínima por hora um pedido ainda pode ser aceito.
Os sliders **Valor pedido mínimo** e **Valor pedido máximo** definem o intervalo de valores sorteados para cada pedido na simulação. Os valores selecionados ficam visíveis ao lado de cada controle.
O gráfico "renda_total_agentes" agora mostra uma linha para cada agente com a renda acumulada somada dia após dia, possibilitando avaliar a evolução individual ao longo da simulação.

