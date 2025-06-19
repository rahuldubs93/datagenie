#Provider
variable "profile" {
  description = "AWS Credentials you want to use"
  default     = "default"
}
variable "region" {
  default = "us-east-1"
}
variable "project" {
  description = "Name of the project"
  default     = "datagenie"
}
variable "environment" {
  description = "The environment for datagenie"
  default     = "go"
}
variable "ecr_image_url" {
  type        = string
  description = "Name of the ECR for datagenie"
}
#ECS
variable "ecs_cluster_name" {
  type        = string
  description = "Name of the ECS cluster for datagenie"
}
variable "allow_all_cidr" {
  type        = string
  description = "CIDR block which allow  IP"
  default = "38.99.100.7/32"
}
variable "vpc_common" {
  type        = string
  description = "Common VPC id that used across services"
}
variable "image_tag" {
  type        = string
  description = "ImageTag"
}
variable "subnet_common" {
  type        = list(string)
  description = "Common subnet id that used across services"
}
variable "us_office_vpn_block" {
  description = "US office VPN"
  type        = string
}
variable "subnet_east1b" {
  type        = string
  description = "Subnet used in east-1b with common VPC"
}
variable "subnet_east1c" {
  type        = string
  description = "Subnet used in east-1c with common VPC"
}
#Roles
variable "ecs_instance_role" {
  description = "ECS Instance role name"
  type        = string
}
variable "ecs_task_execution_role" {
  description = "ECS Execution role name"
  type        = string
}
variable "datagenie_task_def_task_mem" {
  type        = number
  description = "Task memory used in  datagenie Upgrade webserver task definition"
  default = 2048
}
variable "datagenie_task_def_task_cpu" {
  type        = number
  description = " Task Container name for datagenie Upgrade webserver used in task definition"
  default = 1024
}
#Service
variable "datagenie_ecs_service_name" {
  type        = string
  description = " ECS Service for datagenie Webserver"
  default = "datagenie"
}
variable "web_task_def_cont_port" {
  type        = number
  description = "Container Port for Task definition"
  default     = 80
}
variable "scheduling_strategy" {
  type        = string
  description = "Default scheduling strategy"
  default     = "REPLICA"
}
variable "propagate_tags" {
  type        = string
  description = "Default propagate tags from application"
  default     = "TASK_DEFINITION"
}
variable "lb_datagenie_target_port_web" {
  type        = number
  description = "Load balancer port for datagenie target group"
  default = 8080
}
#Load balancer Listener
variable "https_port" {
  description = "Port used in Https"
  type        = number
  default = 443
}
variable "ssl_policy" {
  description = "Default policies provided by elastic load balancing to application load balancer"
  type = string
  default = "ELBSecurityPolicy-2016-08"
}
#Route53
variable "team_route53_zone" {
  type        = string
  description = "ProdZone ID defined for data team"
}
variable "datagenie_dns_name" {
  type        = string
  description = " DNS name for datagenie upgrade"
}
#IAM Certificate Server
variable "datagenie_certificate_name_web" {
    description = " datagenie Certificate name"
    type = string
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(any)
  default     = {}
}

variable "autoscale_web" {
  description = "Autoscale configuration"
  type = object({
    max_capacity = number
    min_capacity = number
    metrics = map(
      object({
        actions_enabled         = optional(bool, true)
        adjustment_type         = string
        cooldown                = optional(number, null)
        datapoints_to_alarm     = optional(number, null)
        evaluation_periods      = number
        metric_aggregation_type = string
        period                  = number
        statistic               = string
        # TODO: Validate that either lower or upper bound are non-null.
        down = object({
          comparison_operator         = string
          metric_interval_lower_bound = optional(number, null)
          metric_interval_upper_bound = optional(number, null)
          scaling_adjustment          = number
          threshold                   = number
        })
        # TODO: Validate that either lower or upper bound are non-null.
        up = object({
          comparison_operator         = string
          metric_interval_lower_bound = optional(number, null)
          metric_interval_upper_bound = optional(number, null)
          scaling_adjustment          = number
          threshold                   = number
        })
      })
    )
  })
  default = null

  validation {
    condition     = var.autoscale_web == null || try(length(var.autoscale_web.metrics) > 0, true)
    error_message = "The 'autoscale' block must have one or more metrics"
  }
}