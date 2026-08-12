variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "Ubuntu Server AMI"
  type        = string
  default     = "ami-0b6d9d3d33ba97d99"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
  default     = "vpc-074e3b599582e2a53"
}

variable "subnet_id" {
  description = "Existing subnet ID"
  type        = string
  default     = "subnet-0c0d52351aae087ac"
}

variable "security_group_id" {
  description = "Existing security group ID"
  type        = string
  default     = "sg-011e2faa66cacbcc0"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name"
  type        = string
}
