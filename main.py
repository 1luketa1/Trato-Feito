import Services.NeoService as neo
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "API funcionando"}

'''
neo.CreatePerson("Carlinhos, O ultimo domador de cavalos", "TestPer1")
neo.CreateTrack("Subida Descida Subida Descida", "TestTra1")
neo.CreateHorse("GABRIEL, O INDOMAVEL", "TestHor1")
neo.CreateHorse("CAVALO COM TATUAGEM DO LINKINPARK", "TestHor2")
neo.CreateDeposit(2050.00, "TestPer1", "TestDep1")
neo.CreateRun(datetime.now(), ["TestHor2", "TestHor1"], "TestTra1", "TestRun1")
neo.CreateViewedRunRelation("TestPer1", "TestRun1")
neo.CreateFavoriteRunRelation("TestPer1", "TestRun1")
neo.CreateViewedHorseRelation("TestPer1", "TestHor1")
neo.CreateFavoriteHorseRelation("TestPer1", "TestHor1")
neo.CreateViewedTrackRelation("TestPer1", "TestTra1")
neo.CreateFavoriteTrackRelation("TestPer1", "TestTra1")
neo.CreateTicket(2050.00, "TestPer1", "TestRun1", "TestTic1")

print(neo.ReadPerson("TestPer1"))
print(neo.ReadTrack("TestTra1"))
print(neo.ReadHorse("TestHor1"))
print(neo.ReadHorse("TestHor2"))
print(neo.ReadDeposit("TestDep1"))
print(neo.ReadRun("TestRun1"))
print(neo.ReadTicket("TestTic1"))'''

