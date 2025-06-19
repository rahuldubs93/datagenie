# Task execution Role for ECS
data "aws_iam_role" "ecs_task_execution_role" {
  name = var.ecs_task_execution_role
}
# ECS Instance Role
data "aws_iam_role" "ecs_instance_role" {
  name = var.ecs_instance_role
}

data "aws_caller_identity" "current" {}

#ACM Certs
data "aws_acm_certificate" "datagenie_certificate_web" {
  domain   = "${var.datagenie_certificate_name_web}"
  types       = ["IMPORTED"]
  most_recent = true
}