terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "ef457ddc-8dfc-47cc-bc6a-3b475c61ec83"
}

resource "azurerm_resource_group" "rg" {
  name     = "AIR_QUALITY"
  location = "polandcentral"
}
