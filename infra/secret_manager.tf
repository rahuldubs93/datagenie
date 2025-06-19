resource "aws_secretsmanager_secret" "database_url" {
  name = "datagenie/${title(var.environment)}/database_url"
}
resource "aws_secretsmanager_secret" "chatbot_message_url" {
  name = "datagenie/${title(var.environment)}/chatbot_message_url"
}
resource "aws_secretsmanager_secret" "chatbot_token_url" {
  name = "datagenie/${title(var.environment)}/chatbot_token_url"
}
resource "aws_secretsmanager_secret" "chatbot_secret" {
  name = "datagenie/${title(var.environment)}/chatbot_secret"
}
resource "aws_secretsmanager_secret" "robot_jid" {
  name = "datagenie/${title(var.environment)}/robot_jid"
}