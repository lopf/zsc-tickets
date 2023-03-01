import logging
import datetime

import azure.functions as func

from fetch import getEvents
import json
import uuid


def main(myTimer: func.TimerRequest, doc: func.Out[func.Document]) -> None:
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if myTimer.past_due:
        logging.info('The timer is past due!')
    # fresh events, otherwise its somehow persisted
    events = []
    events = getEvents()
    events_json = json.dumps(events)

    document = {
        'id': str(uuid.uuid4()),
        'value': events_json
    }

    cosmosdb_events = func.DocumentList()
    cosmosdb_events.append(document)

    doc.set(cosmosdb_events)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
