locals {
  environment_values = {
    Key = "Value"
  }
  # secret_values = {
  #   SecretKey = "${data.aws_secretsmanager_secret.<key>.arn}"
  # }
}

resource "aws_ecs_task_definition" "datagenie_td" {
  family             = "${var.environment}-${var.ecs_cluster_name}-${var.datagenie_ecs_service_name}"
  task_role_arn      = data.aws_iam_role.ecs_task_execution_role.arn
  execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
  container_definitions = jsonencode([
    {
      name  = "${var.datagenie_ecs_service_name}"
      image = "${var.ecr_image_url}:${var.image_tag}"
      cpu       = var.datagenie_task_def_task_cpu
      memory    = var.datagenie_task_def_task_mem
      essential = true
      portMappings = [
        {
          containerPort = 80
          protocol      = "tcp"
          hostPort      = 80
        }
      ]

      # command = ["datagenie"]
      environment = [
        for k, v in "${local.environment_values}" : {
          name  = k
          value = v

        }
      ]

      # secrets = [
      #   for k, v in "${local.secret_values}" : {
      #     name      = k
      #     valueFrom = v

      #   }
      # ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "${aws_cloudwatch_log_group.datagenie.name}"
          awslogs-region        = "${var.region}"
          awslogs-stream-prefix = "${var.datagenie_ecs_service_name}"
        }
      }
    }
  ])

  cpu                      = var.datagenie_task_def_task_cpu
  memory                   = var.datagenie_task_def_task_mem
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  runtime_platform {
    operating_system_family = "LINUX"
  }
  tags = {
    Name        = "${var.environment} datagenie "
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}

