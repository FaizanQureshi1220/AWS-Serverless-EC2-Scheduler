# AWS Serverless Cost Optimization EC2-Scheduler

This project implements a cost-saving automation solution for AWS EC2 instances. It uses Infrastructure as Code (IaC) with Terraform to deploy a serverless scheduler that automatically starts an EC2 instance in the morning and stops it in the evening, ensuring the instance only runs during business hours.

## 🛠️ Technology Stack

  * **Infrastructure as Code (IaC):** Terraform (`.tf` files)
  * **Scheduling:** AWS EventBridge (Cron rules)
  * **Execution:** AWS Lambda (Python 3.9)
  * **AWS SDK:** Boto3 (Python library for EC2 management)

## 🚀 Deployment

### Prerequisites

1.  **AWS CLI Configured:** Your local machine must have AWS credentials configured (via `aws configure`). The user must have `AdministratorAccess` or equivalent permissions, including `iam:PassRole`, to deploy these resources.
2.  **Terraform Installed:** Terraform CLI must be installed on your system.
3.  **Python Script:** The `EC2-Toggle.py` script must exist in the root directory.

### Configuration

You must provide your specific AWS details using a Terraform variables file.

1.  Create a file named **`terraform.tfvars`** in the project's root directory.
2.  Add the following variables to the file, replacing the placeholder values with your actual ARN and ID:

<!-- end list -->

```terraform
# The ARN of the existing IAM Role used by the Lambda function.
# This role MUST have permissions to start/stop EC2 instances and write to CloudWatch.
lambda_role_arn = "arn:aws:iam::123456789012:role/YourExistingLambdaExecutionRole"

# The ID of the EC2 instance you want to manage.
instance_id = "i-0abcdef1234567890" 

# Optional: Override default times (0 8 * * ? * = 8:00 AM UTC)
# start_time = "0 8 * * ? *" 
# stop_time = "0 20 * * ? *"
