resource "azurerm_application_insights" "zsc-ticketalerts" {
  name                = "tf-test-appinsights"
  location            = azurerm_resource_group.zsc-ticketalerts.location
  resource_group_name = azurerm_resource_group.zsc-ticketalerts.name
  application_type    = "other"
}
