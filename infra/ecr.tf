# resource "aws_ecr_repository" "datagenie_ecr" {
#   name                 = "${var.ecs_cluster_name}-ecr"
#   image_tag_mutability = "MUTABLE"

#   image_scanning_configuration {
#     scan_on_push = true
#   }
#   tags = {
#     Name        = "${var.environment} datagenie Upgrade ECR Repository"
#     Project     = "${var.project}"
#     Environment = "${var.environment}"
#   }
# }
