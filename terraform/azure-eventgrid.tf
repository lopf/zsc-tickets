resource "azurerm_storage_queue" "zsc-ticketalerts" {
  name                 = "zsc-ticketalerts"
  storage_account_name = azurerm_storage_account.zsc-ticketalerts.name
}

resource "azurerm_eventgrid_topic" "zsc-ticketalerts" {
  name                = "zsc-ticketalerts-topic"
  location            = azurerm_resource_group.zsc-ticketalerts.location
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
}

resource "azurerm_eventgrid_event_subscription" "zsc-ticketalerts" {
  name  = "zsc-ticketalerts-storage-queue-subscription"
  scope = azurerm_eventgrid_topic.zsc-ticketalerts.id

  storage_queue_endpoint {
    storage_account_id = azurerm_storage_account.zsc-ticketalerts.id
    queue_name         = azurerm_storage_queue.zsc-ticketalerts.name
  }
}
