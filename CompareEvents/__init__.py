import logging

# CosmosDB Client
from azure.cosmos import CosmosClient

# Event Grid Client
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential

import azure.functions as func
import os
import datetime


def main(documents: func.DocumentList) -> None:
    # if documents:
    #    logging.warn("Triggered by new or modified document, ignoring...")
    #    return

    connection_string = os.environ['AzureCosmosDBConnectionString']

    # Create a Cosmos DB client using the connection string
    client = CosmosClient.from_connection_string(conn_str=connection_string)

    database_name = os.environ.get('MyCosmosDbName')
    container_name = os.environ.get('MyCosmosDbCollection')

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    query = "SELECT TOP 2 * FROM c ORDER BY c._ts DESC"
    results = container.query_items(query, enable_cross_partition_query=True)

    documents = list(results)
    logging.info("Found %d documents", len(documents))

    if len(documents) < 2:
        logging.info("Not enough documents to compare.")
        return

    latest_values = [documents[0]["value"], documents[1]["value"]]
    logging.info("Latest values: %s", latest_values)

    if latest_values[0] == latest_values[1]:
        logging.info("Latest two values are the same: %s", latest_values)
    else:
        logging.info("Latest two values are different: %s", latest_values)

        logging.info("Send to Event Grid")

        topic_key = os.environ["MyEventGridTopicKeySetting"]
        endpoint = os.environ["MyEventGridTopicUriSetting"]
        credential = AzureKeyCredential(topic_key)
        client = EventGridPublisherClient(endpoint, credential)
        # publish event

        client.send([
            EventGridEvent(
                    event_type="EventsUpdated",
                    data={
                        "message": "Content changed, new events are published!"
                    },
                    subject="Events Updated",
                    data_version="2.0",
                    event_time=datetime.datetime.now()
                    )
        ])
        print("Published events to Event Grid.")
