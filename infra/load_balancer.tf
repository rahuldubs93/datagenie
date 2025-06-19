# Create load balancer for ECS fargate service
resource "aws_lb" "datagenie_ecs_lb_web" {
  name               = "${var.environment}-${var.ecs_cluster_name}-web-lb"
  internal           = false
  load_balancer_type = "application"
  ip_address_type    = "ipv4"
  security_groups    = ["${aws_security_group.datagenie_load_balancer_sg.id}"]
  subnets            = ["${var.subnet_east1c}", "${var.subnet_east1b}"]
  idle_timeout       = 900

  tags = {
    Name        = "${var.environment} Load Balancer for datagenie Webserver"
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}

