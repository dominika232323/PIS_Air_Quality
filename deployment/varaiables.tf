variable "subscription" {
  description = "id your of azure subscription"
  type = string
}

variable "admin_username" {
  description = "Administrator username for the VMs"
  type        = string
  default     = "azureuser"
}

variable "admin_password" {
  description = "Administrator password for the VMs"
  type        = string
  default     = "ChangeMe123!"
}

variable "open_ports" {
  description = "List of ports to open in the Network Security Group"
  type        = list(number)
  default     = [22, 80]
}