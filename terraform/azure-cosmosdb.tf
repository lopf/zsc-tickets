resource "azurerm_cosmosdb_account" "zsc-ticketalerts" {
  location            = azurerm_resource_group.zsc-ticketalerts.location
  name                = "eventsdb"
  offer_type          = "Standard"
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
  tags = {
    defaultExperience       = "Core (SQL)"
    hidden-cosmos-mmspecial = ""
  }
  consistency_policy {
    consistency_level = "Session"
  }
  geo_location {
    failover_priority = 0
    location          = azurerm_resource_group.zsc-ticketalerts.location
  }
  capabilities {
    name = "EnableServerless"
  }
}

resource "azurerm_cosmosdb_sql_container" "zsc-ticketalerts" {
  account_name          = azurerm_cosmosdb_account.zsc-ticketalerts.name
  database_name         = var.cosmosdb_name
  name                  = var.cosmosdb_collection
  partition_key_path    = "/id"
  partition_key_version = 2
  resource_group_name   = azurerm_resource_group.zsc-ticketalerts.name
  depends_on = [
    azurerm_cosmosdb_sql_database.zsc-ticketalerts
  ]
}
resource "azurerm_cosmosdb_sql_database" "zsc-ticketalerts" {
  account_name        = azurerm_cosmosdb_account.zsc-ticketalerts.name
  name                = var.cosmosdb_name
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
  depends_on = [
    azurerm_cosmosdb_account.zsc-ticketalerts
  ]
}
