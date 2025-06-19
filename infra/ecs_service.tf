# datagenie Webserver Service
resource "aws_ecs_service" "datagenie_webserver_service" {
  name                = var.datagenie_ecs_service_name
  cluster             = "${var.environment}-${var.ecs_cluster_name}-ecs"
  desired_count       = 1
  task_definition     = aws_ecs_task_definition.datagenie_td.arn
  scheduling_strategy = var.scheduling_strategy
  launch_type         = "FARGATE"
  deployment_maximum_percent = 200
  deployment_minimum_healthy_percent = 100

  network_configuration {
    subnets          = var.subnet_common
    security_groups  = [aws_security_group.datagenie_load_balancer_sg.id]
  }

  health_check_grace_period_seconds = 1800

  load_balancer {
    target_group_arn = aws_lb_target_group.datagenie_target_group_web.arn
    container_name   = var.datagenie_ecs_service_name
    container_port   = var.web_task_def_cont_port
  }
  enable_ecs_managed_tags = true
  propagate_tags          = var.propagate_tags
  tags = {
    Name        = "${var.ecs_cluster_name} Service"
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}
