output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.quantum_safe_server.id
}

output "public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.quantum_safe_server.public_ip
}

output "public_dns" {
  description = "EC2 public DNS"
  value       = aws_instance.quantum_safe_server.public_dns
}

output "ssh_command" {
  description = "SSH command"
  value       = "ssh -i terraform-kp.pem ubuntu@${aws_instance.quantum_safe_server.public_ip}"
}
