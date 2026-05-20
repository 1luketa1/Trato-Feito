from fastapi import FastAPI
from cavalo import router as cavalos_router
from corridas import router as corridas_router
from pistas import router as resultados_router
from pistas import router as pistas_router

app = FastAPI()


app.include_router(cavalos_router)
app.include_router(corridas_router)
app.include_router(resultados_router)
app.include_router(pistas_router)
@app.get("/")
def home():
    return {"msg": "API funcionando"}