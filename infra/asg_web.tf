# locals {
#   autoscale_metrics_web = { for k in try(keys(var.autoscale_web.metrics), {}) : k => var.autoscale_web.metrics[k] }
# }

# # Autoscaling target.

# # TODO: Study (and document) how min_capacity and max_capacity interact with scaleable_dimension.

# resource "aws_appautoscaling_target" "web" {
#   for_each = var.autoscale_web != null ? { autoscale_web = var.autoscale_web } : {}

#   max_capacity       = each.value.max_capacity
#   min_capacity       = each.value.min_capacity
#   resource_id        = format("service/%s/%s", aws_ecs_cluster.datagenie_ecs_cluster.name, aws_ecs_service.datagenie_webserver_service.name)
#   role_arn           = format("arn:aws:iam::%s:role/aws-service-role/ecs.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_ECSService", data.aws_caller_identity.current.account_id)
#   scalable_dimension = "ecs:service:DesiredCount"
#   service_namespace  = "ecs"
# }

# # Scale-down alarm for each metric.

# resource "aws_cloudwatch_metric_alarm" "web_down" {
#   for_each = local.autoscale_metrics_web

#   actions_enabled     = each.value.actions_enabled
#   alarm_actions       = [aws_appautoscaling_policy.web_down[each.key].arn]
#   alarm_description   = format("scale-down alarm for %s on %s metric", aws_ecs_service.datagenie_webserver_service.name, each.key)
#   alarm_name          = format("ecs-%s-%s-down", aws_ecs_service.datagenie_webserver_service.name, lower(each.key))
#   comparison_operator = each.value.down.comparison_operator
#   datapoints_to_alarm = each.value.datapoints_to_alarm
#   evaluation_periods  = each.value.evaluation_periods
#   metric_name         = each.key
#   namespace           = "AWS/ECS"
#   period              = each.value.period
#   statistic           = each.value.statistic
#   tags                = merge({ Name = var.ecs_cluster_name},{ env = var.environment}, var.tags)
#   threshold           = each.value.down.threshold

#   dimensions = {
#     ClusterName = aws_ecs_cluster.datagenie_ecs_cluster.name
#     ServiceName = aws_ecs_service.datagenie_webserver_service.name
#   }
# }

# # Scale-up alarm for each metric.

# resource "aws_cloudwatch_metric_alarm" "web_up" {
#   for_each = local.autoscale_metrics_web

#   actions_enabled     = each.value.actions_enabled
#   alarm_actions       = [aws_appautoscaling_policy.web_up[each.key].arn]
#   alarm_description   = format("scale-up alarm for %s on %s metric", aws_ecs_service.datagenie_webserver_service.name, each.key)
#   alarm_name          = format("ecs-%s-%s-up", aws_ecs_service.datagenie_webserver_service.name, lower(each.key))
#   comparison_operator = each.value.up.comparison_operator
#   datapoints_to_alarm = each.value.datapoints_to_alarm
#   evaluation_periods  = each.value.evaluation_periods
#   metric_name         = each.key
#   namespace           = "AWS/ECS"
#   period              = each.value.period
#   statistic           = each.value.statistic
#   tags                = merge({ Name = var.ecs_cluster_name},{ env = var.environment}, var.tags)
#   threshold           = each.value.up.threshold

#   dimensions = {
#     ClusterName = aws_ecs_cluster.datagenie_ecs_cluster.name
#     ServiceName = aws_ecs_service.datagenie_webserver_service.name
#   }
# }

# # Scale-down policy for each metric.

# resource "aws_appautoscaling_policy" "web_down" {
#   for_each = local.autoscale_metrics_web

#   name               = format("ecs-%s-%s-down", aws_ecs_service.datagenie_webserver_service.name, lower(each.key))
#   resource_id        = aws_appautoscaling_target.web["autoscale_web"].resource_id
#   scalable_dimension = aws_appautoscaling_target.web["autoscale_web"].scalable_dimension
#   service_namespace  = aws_appautoscaling_target.web["autoscale_web"].service_namespace

#   step_scaling_policy_configuration {
#     adjustment_type         = each.value.adjustment_type
#     cooldown                = each.value.cooldown
#     metric_aggregation_type = each.value.metric_aggregation_type

#     step_adjustment {
#       metric_interval_lower_bound = each.value.down.metric_interval_lower_bound
#       metric_interval_upper_bound = each.value.down.metric_interval_upper_bound
#       scaling_adjustment          = each.value.down.scaling_adjustment
#     }
#   }
# }

# # Scale-up policy for each metric.

# resource "aws_appautoscaling_policy" "web_up" {
#   for_each = local.autoscale_metrics_web

#   name               = format("ecs-%s-%s-up", aws_ecs_service.datagenie_webserver_service.name, lower(each.key))
#   resource_id        = aws_appautoscaling_target.web["autoscale_web"].resource_id
#   scalable_dimension = aws_appautoscaling_target.web["autoscale_web"].scalable_dimension
#   service_namespace  = aws_appautoscaling_target.web["autoscale_web"].service_namespace

#   step_scaling_policy_configuration {
#     adjustment_type         = each.value.adjustment_type
#     cooldown                = each.value.cooldown
#     metric_aggregation_type = each.value.metric_aggregation_type

#     step_adjustment {
#       metric_interval_lower_bound = each.value.up.metric_interval_lower_bound
#       metric_interval_upper_bound = each.value.up.metric_interval_upper_bound
#       scaling_adjustment          = each.value.up.scaling_adjustment
#     }
#   }
# }