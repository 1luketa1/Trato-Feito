import random
from services.odds_services import gerar_odds_corrida


def simular_corrida(corrida_id):

    odds_data = gerar_odds_corrida(corrida_id)

    if not odds_data:
        return None

    probabilidades = odds_data["probabilidades"]

    cavalos = list(probabilidades.keys())
    pesos = list(probabilidades.values())

    # 🎯 sorteio ponderado
    vencedor = random.choices(
        cavalos,
        weights=pesos,
        k=1
    )[0]

    # ranking completo (ordenado por score)
    ranking = sorted(
        probabilidades.items(),
        key=lambda x: x[1],
        reverse=True
    )

    resultado = []

    posicao = 1

    for cavalo_id, _ in ranking:

        resultado.append({
            "cavalo_id": cavalo_id,
            "posicao": posicao,
            "tempo": round(random.uniform(110, 130), 2)
        })

        posicao += 1

    return {
        "vencedor": vencedor,
        "resultado": resultado
    }