import json
from neo4j import GraphDatabase 
from datetime import datetime

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

def CreateTicket(value, buyerDBAcessKey, runDBAcessKey, horseBetDBAcessKey, dBAcessKey):
    
    '''
    FUTURE OPTIMIZATION:

    (Person)-[:PlacedBetOn {times}]->(Horse)
    (Person)-[:BetOnTrack {times}]->(Track)
    '''

    query = """
    MATCH (p:Person {
        dBAcessKey:$buyerDBAcessKey
    })

    MATCH (r:Run {
        dBAcessKey:$runDBAcessKey
    })

    MATCH (h:Horse {
        dBAcessKey:$horseBetDBAcessKey
    })

    MERGE (t:Ticket {
        dBAcessKey:$dBAcessKey
    })

    SET t.value = $value

    MERGE (p)-[:Bought]->(t)

    MERGE (t)-[:References]->(r)

    MERGE (t)-[:BetsOn]->(h)
    """

    with driver.session() as session:

        session.run(
            query,
            value=value,
            buyerDBAcessKey=buyerDBAcessKey,
            runDBAcessKey=runDBAcessKey,
            horseBetDBAcessKey=horseBetDBAcessKey,
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

    MERGE (p)-[v:Viewed]->(h)

    ON CREATE SET v.times = 1

    ON MATCH SET v.times = v.times + 1
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

    MERGE (p)-[v:Viewed]->(r)

    ON CREATE SET v.times = 1

    ON MATCH SET v.times = v.times + 1
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

    MERGE (p)-[v:Viewed]->(t)

    ON CREATE SET v.times = 1

    ON MATCH SET v.times = v.times + 1
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

'''
IDEAS

Tracks a horse likes

'''

# ===========
# PersonHorse
# ===========

def FilterByPersonFavoriteHorses(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(h:Horse)

    RETURN h

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "horse": dict(data["h"])
            }
            for data in result
        ]


def FilterByPersonMostViewedHorses(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(h:Horse)

    RETURN h, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "horse": dict(data["h"]),
                "views": data["views"]
            }
            for data in result
        ]


# ===========
# PersonTrack
# ===========

def FilterByPersonFavoriteTracks(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(t:Track)

    RETURN t

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "track": dict(data["t"])
            }
            for data in result
        ]


def FilterByPersonMostViewedTracks(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(t:Track)

    RETURN t, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "track": dict(data["t"]),
                "views": data["views"]
            }
            for data in result
        ]


# ===========
# AllTimeRuns
# ===========

def FilterByRunsHorseIsIn(horseDBAcessKey, limit):

    query = """
    MATCH (h:Horse {
        dBAcessKey:$horseDBAcessKey
    })-[:RacesIn]->(r:Run)

    RETURN r

    ORDER BY r.date ASC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            horseDBAcessKey=horseDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByAllRunsTrackIsIn(trackDBAcessKey, limit):

    query = """
    MATCH (r:Run)-[:OccursAt]->(t:Track {
        dBAcessKey:$trackDBAcessKey
    })

    RETURN r

    ORDER BY r.date ASC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            trackDBAcessKey=trackDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByMostViewedOpenRuns(limit):

    query = """
    MATCH (:Person)-[v:Viewed]->(r:Run)

    WHERE r.date > datetime()

    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByAllMostBuyedRuns(limit):

    query = """
    MATCH (:Person)-[:Bought]->(:Ticket)-[:References]->(r:Run)

    RETURN r, count(*) AS buys

    ORDER BY buys DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "buys": data["buys"]
            }
            for data in result
        ]


def FilterByPersonMostViewedTracksAllRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(t:Track)<-[:OccursAt]-(r:Run)
    
    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByPersonFavoriteTracksAllRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person { dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(t:Track)<-[:OccursAt]-(r:Run)

    RETURN r

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByPersonMostViewedHorsesAllRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(h:Horse)-[:RacesIn]->(r:Run)

    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByPersonFavoriteHorsesAllRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(h:Horse)-[:RacesIn]->(r:Run)

    RETURN r

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


# =========
# OpenRuns
# =========

def FilterByOpenRunsHorseIsIn(horseDBAcessKey, limit):

    query = """
    MATCH (h:Horse {
        dBAcessKey:$horseDBAcessKey
    })-[:RacesIn]->(r:Run)

    WHERE r.date > datetime()

    RETURN r

    ORDER BY r.date ASC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            horseDBAcessKey=horseDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByOpenRunsTrackIsIn(trackDBAcessKey, limit):

    query = """
    MATCH (r:Run)-[:OccursAt]->(t:Track {
        dBAcessKey:$trackDBAcessKey
    })

    WHERE r.date > datetime()

    RETURN r

    ORDER BY r.date ASC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            trackDBAcessKey=trackDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByAllMostViewedRuns(limit):

    query = """
    MATCH (:Person)-[v:Viewed]->(r:Run)

    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByOpenMostBuyedRuns(limit):

    query = """
    MATCH (:Person)-[:Bought]->(:Ticket)-[:References]->(r:Run)

    WHERE r.date > datetime()

    RETURN r, count(*) AS buys

    ORDER BY buys DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "buys": data["buys"]
            }
            for data in result
        ]


def FilterByPersonMostViewedTracksOpenRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(t:Track)<-[:OccursAt]-(r:Run)

    WHERE r.date > datetime()

    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByPersonFavoriteTracksOpenRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(t:Track)<-[:OccursAt]-(r:Run)

    WHERE r.date > datetime()

    RETURN r

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]


def FilterByPersonMostViewedHorsesOpenRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[v:Viewed]->(h:Horse)-[:RacesIn]->(r:Run)

    WHERE r.date > datetime()

    RETURN r, sum(v.times) AS views

    ORDER BY views DESC

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"]),
                "views": data["views"]
            }
            for data in result
        ]


def FilterByPersonFavoriteHorsesOpenRuns(personDBAcessKey, limit):

    query = """
    MATCH (p:Person {
        dBAcessKey:$personDBAcessKey
    })-[:Favorited]->(h:Horse)-[:RacesIn]->(r:Run)

    WHERE r.date > datetime()

    RETURN r

    LIMIT $limit
    """

    with driver.session() as session:

        result = session.run(
            query,
            personDBAcessKey=personDBAcessKey,
            limit=limit
        )

        return [
            {
                "run": dict(data["r"])
            }
            for data in result
        ]