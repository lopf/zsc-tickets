provider "azurerm" {
  features {
    # workaround for bug https://github.com/hashicorp/terraform-provider-azurerm/issues/18026
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

resource "azurerm_resource_group" "zsc-ticketalerts" {
  name     = "zsc-ticketalerts-rg"
  location = "West Europe"
}

resource "azurerm_storage_account" "zsc-ticketalerts" {
  name                     = "zscticketalertssa"
  resource_group_name      = azurerm_resource_group.zsc-ticketalerts.name
  location                 = azurerm_resource_group.zsc-ticketalerts.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
