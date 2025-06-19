
# Get zone id of data team hosted zone

data "aws_route53_zone" "team_hosted_zone" {
  name = var.team_route53_zone
}


resource "aws_route53_record" "datagenie_ecs_dns" {
  zone_id = data.aws_route53_zone.team_hosted_zone.zone_id
  type    = "A"
  name    = var.datagenie_dns_name

  alias {
    name                   = aws_lb.datagenie_ecs_lb_web.dns_name
    zone_id                = aws_lb.datagenie_ecs_lb_web.zone_id
    evaluate_target_health = false
  }
  depends_on = [
    aws_lb.datagenie_ecs_lb_web
  ]
}
