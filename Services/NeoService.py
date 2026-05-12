import json
from neo4j import GraphDatabase 

with open("InvisibleKeys/NeoKey.json", "r") as arc:
    NeoKey = json.load(arc)

driver = GraphDatabase.driver(
    NeoKey["URI"],
    auth=(NeoKey["USERNAME"], NeoKey["PASSWORD"])
)

# =========================  
#          CREATE
# =========================

#THE KEYS ARE FOR ACESSING DATA IN OTHER DBs
def CreatePerson(name, dBAcessKey):
    query = "MERGE (p:Person {name:$name, dBAcessKey:$dBAcessKey})"

    with driver.session() as session:
        session.run(query, name=name, dBAcessKey=dBAcessKey)

def CreateTicket(value, buyerDBAcessKey, runDBAcessKey, dBAcessKey):

    query = """
    MATCH (p:Person {dBAcessKey:$buyerDBAcessKey})

    MATCH (r:Run {dBAcessKey:$runDBAcessKey})

    MERGE (t:Ticket {
        value:$value,
        dBAcessKey:$dBAcessKey
    })

    MERGE (p)-[:Bought]->(t)
    MERGE (t)-[:GamblesOn]->(r)
    """

    with driver.session() as session:

        session.run(
            query,
            value=value,
            buyerDBAcessKey=buyerDBAcessKey,
            runDBAcessKey=runDBAcessKey,
            dBAcessKey=dBAcessKey
        )


def CreateDeposit(value, buyerdBAcessKey, dBAcessKey):

    query = """
    MATCH (p:Person {dBAcessKey:$buyerdBAcessKey})

    MERGE (d:Deposit {
        dBAcessKey:$dBAcessKey
    })
    SET d.value = $value

    MERGE (p)-[:Deposited]->(t)
    """

    with driver.session() as session:

        session.run(
            query,
            value=value,
            buyerdBAcessKey=buyerdBAcessKey,
            dBAcessKey=dBAcessKey
        )


def CreateHorse(name, dBAcessKey):

    query = """
    MERGE (h:Horse {
        name:$name,
        dBAcessKey:$dBAcessKey
    })
    """

    with driver.session() as session:

        session.run(
            query,
            name=name,
            dBAcessKey=dBAcessKey
        )


def CreateTrack(name, dBAcessKey):

    query = """
    MERGE (t:Track {
        name:$name,
        dBAcessKey:$dBAcessKey
    })
    """

    with driver.session() as session:

        session.run(
            query,
            name=name,
            dBAcessKey=dBAcessKey
        )


#ESSE DAQUI E PERIGOSO TEM QUE TESTA SEPARADO
def CreateRun(date, horsesDBAcessKeys, trackDBAcessKey, dBAcessKey):

    query = """
    MERGE (r:Run {
        dBAcessKey:$dBAcessKey
    })

    SET r.date = $date

    MATCH (t:Track {
        dBAcessKey:$trackDBAcessKey
    })

    MERGE (r)-[:OccursAt]->(t)

    WITH r
    UNWIND $horsesDBAcessKeys AS horseKey

    MATCH (h:Horse {
        dBAcessKey:horseKey
    })

    MERGE (h)-[:RacesIn]->(r)  
    """

    with driver.session() as session:

        session.run(
            query,
            date=date,
            horsesDBAcessKeys=horsesDBAcessKeys,
            trackDBAcessKey=trackDBAcessKey,
            dBAcessKey=dBAcessKey
        )

# =========================
#        RELATIONS
# ========================= 

def CreateViewedHorseRelation(personDBAcessKey, horseDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (h:Horse {
        dBAcessKey:$horseDBAcessKey
    })

    MERGE (p)-[:Viewed]->(h)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            horseDBAcessKey=horseDBAcessKey
        )


def CreateFavoriteHorseRelation(personDBAcessKey, horseDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (h:Horse {
        dBAcessKey:$horseDBAcessKey
    })

    MERGE (p)-[:Favorited]->(h)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            horseDBAcessKey=horseDBAcessKey
        )


def CreateViewedRunRelation(personDBAcessKey, runDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (r:Run {
        dBAcessKey:$runDBAcessKey
    })

    MERGE (p)-[:Viewed]->(r)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            runDBAcessKey=runDBAcessKey
        )


def CreateFavoriteRunRelation(personDBAcessKey, runDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (r:Run {
        dBAcessKey:$runDBAcessKey
    })

    MERGE (p)-[:Favorited]->(r)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            runDBAcessKey=runDBAcessKey
        )


def CreateViewedTrackRelation(personDBAcessKey, trackDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (t:Track {
        dBAcessKey:$trackDBAcessKey
    })

    MERGE (p)-[:Viewed]->(t)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            trackDBAcessKey=trackDBAcessKey
        )


def CreateFavoriteTrackRelation(personDBAcessKey, trackDBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })

    MATCH (t:Track {
        dBAcessKey:$trackDBAcessKey
    })

    MERGE (p)-[:Favorited]->(t)
    """

    with driver.session() as session:

        session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            trackDBAcessKey=trackDBAcessKey
        )

# =========================     
#          UPDATE
# =========================

def UpdatePersonName(dBAcessKey, newName):

    query = """
    MATCH (p:Person {
        dBAcessKey:$dBAcessKey
    })

    SET p.name = $newName
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newName=newName
        )


def UpdateHorseName(dBAcessKey, newName):

    query = """
    MATCH (h:Horse {
        dBAcessKey:$dBAcessKey
    })

    SET h.name = $newName
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newName=newName
        )


def UpdateTrackName(dBAcessKey, newName):

    query = """
    MATCH (t:Track {
        dBAcessKey:$dBAcessKey
    })

    SET t.name = $newName
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newName=newName
        )


def UpdateTicketValue(dBAcessKey, newValue):

    query = """
    MATCH (t:Ticket {
        dBAcessKey:$dBAcessKey
    })

    SET t.value = $newValue
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newValue=newValue
        )


def UpdateDepositValue(dBAcessKey, newValue):

    query = """
    MATCH (d:Deposit {
        dBAcessKey:$dBAcessKey
    })

    SET d.value = $newValue
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newValue=newValue
        )


def UpdateRunDate(dBAcessKey, newDate):

    query = """
    MATCH (r:Run {
        dBAcessKey:$dBAcessKey
    })

    SET r.date = $newDate
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey,
            newDate=newDate
        )


# =========================
#          DELETE
# =========================

def DeletePerson(dBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE p
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )


def DeleteHorse(dBAcessKey):

    query = """
    MATCH (h:Horse {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE h
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )


def DeleteTrack(dBAcessKey):

    query = """
    MATCH (t:Track {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE t
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )


def DeleteTicket(dBAcessKey):

    query = """
    MATCH (t:Ticket {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE t
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )


def DeleteDeposit(dBAcessKey):

    query = """
    MATCH (d:Deposit {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE d
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )


def DeleteRun(dBAcessKey):

    query = """
    MATCH (r:Run {
        dBAcessKey:$dBAcessKey
    })

    DETACH DELETE r
    """

    with driver.session() as session:

        session.run(
            query,
            dBAcessKey=dBAcessKey
        )

# =========================
#           READ
# =========================

def ReadPerson(dBAcessKey):

    query = """
    MATCH (p:Person {
        dBAcessKey:$dBAcessKey
    })

    RETURN p
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["p"])


def ReadHorse(dBAcessKey):

    query = """
    MATCH (h:Horse {
        dBAcessKey:$dBAcessKey
    })

    RETURN h
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["h"])


def ReadTrack(dBAcessKey):

    query = """
    MATCH (t:Track {
        dBAcessKey:$dBAcessKey
    })

    RETURN t
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["t"])


def ReadTicket(dBAcessKey):

    query = """
    MATCH (t:Ticket {
        dBAcessKey:$dBAcessKey
    })

    RETURN t
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["t"])


def ReadDeposit(dBAcessKey):

    query = """
    MATCH (d:Deposit {
        dBAcessKey:$dBAcessKey
    })

    RETURN d
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["d"])


def ReadRun(dBAcessKey):

    query = """
    MATCH (r:Run {
        dBAcessKey:$dBAcessKey
    })

    RETURN r
    """

    with driver.session() as session:

        result = session.run(
            query,
            dBAcessKey=dBAcessKey
        )
        data = result.single()
        return dict(data["r"])


# =========================
#          Filter  
# ========================= 
