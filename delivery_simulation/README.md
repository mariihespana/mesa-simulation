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

O script `run.py` executa a simulação por 30 dias para 50 agentes e imprime as estatísticas coletadas. O `server.py` inicia uma interface web com sliders para configurar parâmetros e gráficos para acompanhar a execução.
