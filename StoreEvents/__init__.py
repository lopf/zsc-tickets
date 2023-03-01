import logging

import azure.functions as func

from fetch import getEvents
import json
import uuid


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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

    return func.HttpResponse(events_json, mimetype='application/json')
