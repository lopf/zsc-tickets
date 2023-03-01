resource "azurerm_service_plan" "zsc-ticketalerts" {
  name                = "zsc-ticketalerts-app-service-plan"
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
  location            = azurerm_resource_group.zsc-ticketalerts.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "zsc-ticketalerts" {
  name                = "zsc-ticketalerts-linux-function-app"
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
  location            = azurerm_resource_group.zsc-ticketalerts.location

  storage_account_name       = azurerm_storage_account.zsc-ticketalerts.name
  storage_account_access_key = azurerm_storage_account.zsc-ticketalerts.primary_access_key
  service_plan_id            = azurerm_service_plan.zsc-ticketalerts.id

  connection_string {
    name  = "AzureCosmosDBConnectionString"
    type  = "Custom"
    value = azurerm_cosmosdb_account.zsc-ticketalerts.primary_sql_connection_string
  }

  app_settings = {
    "MyCosmosDbName"             = var.cosmosdb_name
    "MyCosmosDbCollection"       = var.cosmosdb_collection
    "MyEventGridTopicKeySetting" = azurerm_eventgrid_topic.zsc-ticketalerts.primary_access_key
    "MyEventGridTopicUriSetting" = azurerm_eventgrid_topic.zsc-ticketalerts.endpoint
    "MyQueueName"                = azurerm_storage_queue.zsc-ticketalerts.name
    "GMAIL_USERNAME"             = ""
    "GMAIL_PASSWORD"             = ""
    "NOTIFICATION_EMAIL"         = ""
    "AzureCosmosDBConnectionString" = azurerm_cosmosdb_account.zsc-ticketalerts.primary_sql_connection_string
  }

  lifecycle {
    ignore_changes = [
      app_settings
    ]
  }

  site_config {
    ftps_state = "FtpsOnly"
    application_stack {
      python_version = "3.9"
    }
    cors {
      allowed_origins = ["https://portal.azure.com"]
    }

    application_insights_connection_string = azurerm_application_insights.zsc-ticketalerts.connection_string
    application_insights_key               = azurerm_application_insights.zsc-ticketalerts.instrumentation_key

  }

  depends_on = [
    azurerm_cosmosdb_account.zsc-ticketalerts,
    azurerm_eventgrid_topic.zsc-ticketalerts
  ]
}
