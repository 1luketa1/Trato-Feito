import random
from services.odds_services import gerar_odds_corrida


def simular_corrida(corrida_id):

    odds_data = gerar_odds_corrida(corrida_id)

    if not odds_data:
        return None

    probabilidades = odds_data["probabilidades"]

    # 🎯 simulação baseada em performance real (ruído + probabilidade)
    performances = {}

    for cavalo_id, prob in probabilidades.items():
        # quanto maior a probabilidade, melhor a média de performance
        performance = random.gauss(prob, 0.1)
        performances[cavalo_id] = performance

    # 🏁 ranking real da corrida
    ranking = sorted(
        performances.items(),
        key=lambda x: x[1],
        reverse=True
    )

    resultado = []
    posicao = 1

    for cavalo_id, _ in ranking:

        resultado.append({
            "cavalo_id": cavalo_id,
            "posicao": posicao,
            "tempo": round(110 + posicao * random.uniform(0.8, 2.2), 2)
        })

        posicao += 1

    # 🏆 verdadeiro vencedor = primeiro do ranking
    vencedor = ranking[0][0]

    return {
        "vencedor": vencedor,
        "resultado": resultado
    }