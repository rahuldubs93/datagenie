# Create load balancer listener
resource "aws_lb_listener" "datagenie_ecs_listener_web" {
    load_balancer_arn = aws_lb.datagenie_ecs_lb_web.arn
    port = var.https_port
    protocol = "HTTPS"
    ssl_policy = "${var.ssl_policy}"
    certificate_arn = data.aws_acm_certificate.datagenie_certificate_web.arn

    default_action {
      type = "forward"
      target_group_arn = aws_lb_target_group.datagenie_target_group_web.arn
    }

    tags = {
        Name = "${var.environment} datagenie Web Load balancer Listener https"
        Environment = "${var.environment}"
        Project = "${var.project}"
        }  
}

resource "aws_lb_listener" "datagenie_lb_listener_web" {
    load_balancer_arn = aws_lb.datagenie_ecs_lb_web.arn
    port = var.lb_datagenie_target_port_web
    protocol = "HTTP"

    default_action {
        type = "redirect"
        order = 1
        redirect {
            protocol = "HTTPS"
            port = var.https_port
            host = "#{host}"
            path = "/#{path}"
            query = "#{query}"
            status_code = "HTTP_301"
        }
    }

    tags = {
        Name = "${var.environment} datagenie Load balancer Listener"
        Environment = "${var.environment}"
        Project = "${var.project}"
        } 
    }


# Creating Listener rule

resource "aws_lb_listener_rule" "datagenie_ecs_listener_rule_web" {
    listener_arn = aws_lb_listener.datagenie_ecs_listener_web.arn

    action {
      type = "forward"
      target_group_arn = aws_lb_target_group.datagenie_target_group_web.arn
    }

    condition {
      host_header {
          values = ["${aws_route53_record.datagenie_ecs_dns.name}.${var.team_route53_zone}"]
      }
    }
    tags = {
        Name = "${var.environment} datagenie Load balancer Listener Rule"
        Environment = "${var.environment}"
        Project = "${var.project}"
        } 
}