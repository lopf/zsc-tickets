variable "cosmosdb_name" {
  type = string
  description = "The primary name of the CosmosDB"
  default = "eventsdb"
}

variable "cosmosdb_collection" {
  type = string
  description = "The primary name of the CosmosDB"
  default = "eventupdates"
}
