profile = "app-data-science-prod"
datagenie_certificate_name_web = "datagenie.go.zoomdt.corp.zoom.com"
datagenie_dns_name  = "datagenie.go"
image_tag = "zdt_data_api_v1.27"
ecr_image_url = "633687408406.dkr.ecr.us-east-1.amazonaws.com/zdt_data_api"
ecs_cluster_name = "datagenie"
ecs_instance_role = "EcsTaskDatagenieGo"
ecs_task_execution_role = "EcsTaskDatagenieGo"
subnet_common = ["subnet-0ef63383f87f82d1c","subnet-0717e9ba1e8e2c6ae"]
subnet_east1b = "subnet-00e3e17937a6c6993"
subnet_east1c = "subnet-0f8101b711713a113"
team_route53_zone = "zoomdt.corp.zoom.com"
us_office_vpn_block = "10.1.0.0/16"
vpc_common = "vpc-0d7b71d97ab1002fd"
allow_all_cidr = "38.99.100.7/32"
autoscale_web = {
    max_capacity = 5
    min_capacity = 1
    metrics = {
        CPUUtilization = {
        adjustment_type         = "ChangeInCapacity"
        cooldown                = 60
        datapoints_to_alarm     = 1
        evaluation_periods      = 1
        metric_aggregation_type = "Average"
        period                  = 60
        statistic               = "Average"

        down = {
            comparison_operator         = "LessThanThreshold"
            metric_interval_upper_bound = 0
            scaling_adjustment          = -1
            threshold                   = 40
        }

        up = {
            comparison_operator         = "GreaterThanOrEqualToThreshold"
            metric_interval_lower_bound = 1
            scaling_adjustment          = 1
            threshold                   = 70
        }
    }
    }
}
