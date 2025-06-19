# Security group creation for datagenie Load Balancer
resource "aws_security_group" "datagenie_load_balancer_sg" {
  name        = "datagenie Load Balancer ${var.environment} security group"
  description = "Security group for ${var.environment} datagenie Load Balancer"
  vpc_id      = var.vpc_common

  ingress {
    description = "Allow all Security group"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.allow_all_cidr}"]
  }
  ingress {
    description = "Allow all Security group"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["${var.allow_all_cidr}"]
  }
  ingress {
      from_port = 0
      to_port = 0
      protocol = -1
      self = true
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.environment} loadbalancer security group"
    Project = "${var.project}"
  }

}
