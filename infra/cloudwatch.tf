# log group for webserver
resource "aws_cloudwatch_log_group" "datagenie" {
  name              = "/aws/ecs/${var.environment}-datagenie"
  retention_in_days = 180
  tags = {
    Name        = "${var.environment} datagenie Cloudwatch log group"
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}
