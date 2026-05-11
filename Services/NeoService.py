import json
from neo4j import GraphDatabase 

with open("InvisibleKeys/NeoKey.json", "r") as arc:
    NeoKey = json.load(arc)

driver = GraphDatabase.driver(
    NeoKey["URI"],
    auth=(NeoKey["USERNAME"], NeoKey["PASSWORD"])
)

#THE ACESS KEYS ARE FOR FINDING THE DATA IN OTHER DBs
def CreatePerson(name, dBAcessKey):
    query = "MERGE (p:Person {name:$name, dBAcessKey:$dBAcessKey})"

    with driver.session() as session:
        session.run(query, name=name, dBAcessKey=dBAcessKey)

def CreateTicket(ticketId, dBAcessKey):

    query = """
    MERGE (t:Ticket {
        ticketId:$ticketId,
        dBAcessKey:$dBAcessKey
    })
    """

    with driver.session() as session:

        session.run(
            query,
            ticketId=ticketId,
            dBAcessKey=dBAcessKey
        )


def CreateDeposit(depositId, value, dBAcessKey):

    query = """
    MERGE (d:Deposit {
        depositId:$depositId,
        dBAcessKey:$dBAcessKey
    })
    SET d.value = $value
    """

    with driver.session() as session:

        session.run(
            query,
            depositId=depositId,
            value=value,
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


def CreateRun(runId, date, dBAcessKey):

    query = """
    MERGE (r:Run {
        runId:$runId,
        dBAcessKey:$dBAcessKey
    })
    SET r.date = $date
    """

    with driver.session() as session:

        session.run(
            query,
            runId=runId,
            date=date,
            dBAcessKey=dBAcessKey
        )