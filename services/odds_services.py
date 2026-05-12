import random
from model.corrida_model import CorridaModel


def calcular_score_cavalo(cavalo, pista):
    stats = cavalo["estatisticas"]
    estado = cavalo["estado"]
    perfil = cavalo["perfil"]

    score = (
        stats["velocidade_media"] * 0.35 +
        stats["aceleracao"] * 6 * 0.20 +
        stats["resistencia"] * 6 * 0.15 +
        stats["consistencia"] * 100 * 0.10 +
        stats["velocidade_maxima"] * 0.20
    )

    score *= (1 - estado["fadiga"])

    score *= (1 + min(estado["dias_desde_ultima_corrida"], 10) * 0.01)

    if pista and "tipo" in pista:
        if perfil["tipo_pista_preferida"] == pista["tipo"]:
            score *= 1.05

    score *= random.uniform(0.97, 1.03)

    return score


def gerar_odds_corrida(id_corrida):
    corrida = CorridaModel.buscar_corrida(id_corrida)

    if not corrida:
        return None

    pista = corrida.get("pista")
    cavalos = corrida.get("cavalos_info", [])

    if not cavalos:
        return None

    scores = []

    for cavalo in cavalos:
        score = calcular_score_cavalo(cavalo, pista)
        scores.append((cavalo["_id"], score))

    total = sum(score for _, score in scores)

    probabilidades = {
        cavalo_id: score / total
        for cavalo_id, score in scores
    }

    odds = {
        cavalo_id: round(1 / p, 2)
        for cavalo_id, p in probabilidades.items()
    }

    return {
        "corrida_id": id_corrida,
        "probabilidades": probabilidades,
        "odds": odds
    }