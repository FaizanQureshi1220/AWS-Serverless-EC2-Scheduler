variable "region" {

    description = "AWS Region to deploy lambda function"
    type        = string
    default     = "us-east-1"

}


variable "instance_id" {

    description = "This is the Instance Id"
    type = string
  
}


variable "start_time" {
  
    description = "This is the starting time of the EC2 instances"
    type = string
    default = "0 11 * * ? *"

}

variable "stop_time" {
  
    description = "This is the stopping time of the EC2 instances"
    type = string
    default = "3 11 * * ? *"

}


variable "lambda_role_arn" {

    description = "This is the role arn for lambda function"
    type = string
  
}