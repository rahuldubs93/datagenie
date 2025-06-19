# Creating load balancer target group 
resource "aws_lb_target_group" "datagenie_target_group_web" {
  name                 =  "${var.environment}-${var.ecs_cluster_name}-web"
  port                 = var.lb_datagenie_target_port_web
  protocol             = "HTTP"
  target_type          = "ip"
  vpc_id               = var.vpc_common
  deregistration_delay = 60

  health_check {
    path                = "/"
    interval            = "30"
    matcher             = "200"
    healthy_threshold   = 5
    unhealthy_threshold = 10
    timeout             = 10
    protocol            = "HTTP"
  }
  tags = {
    Name        = "${var.environment} Load Balancer Target for datagenie"
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }

}