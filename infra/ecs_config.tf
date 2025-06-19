resource "aws_ecs_cluster" "datagenie_ecs_cluster" {
  name = "${var.environment}-${var.ecs_cluster_name}-ecs"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  tags = {
    Name    = "ECS Cluster for ${var.environment} datagenie"
    Project = "${var.project}"
  }
}
