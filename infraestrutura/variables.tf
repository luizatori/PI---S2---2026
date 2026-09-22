variable "vm_name" {
  type        = string
  default     = "vm-gerador-hardware"
  description = "Nome da vm"
}

variable "memory_mb" {
  type        = number
  default     = 2048
  description = "Quantidade de memoria RAM em MB"
}

variable "vcpu" {
  type        = number
  default     = 2
  description = "Quantidade de vCPUs"
}

variable "disk_size_gb" {
  type        = number
  default     = 20
  description = "Tamanho do disco da VM em GB"
}