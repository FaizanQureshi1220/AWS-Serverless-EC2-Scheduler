
data "archive_file" "zip_file" {

    type        = "zip"
    source_file = "EC2-Toggle.py"
    output_path = "EC2-Toggle.zip"

}

### Main Lambda Function

resource "aws_lambda_function" "EC2_toggler" {
  
    filename = data.archive_file.zip_file.output_path
    function_name = "EC2-Scheduler-${var.instance_id}"
    role = var.lambda_role_arn
    handler = "EC2-Toggle.lambda_handler"
    runtime = "python3.9"
    source_code_hash = data.archive_file.zip_file.output_base64sha256
    timeout = 30

    environment {
        variables = {
            Instance_Id = var.instance_id
        }
    }
}


### Eventbridge Scheduler

resource "aws_cloudwatch_event_rule" "EC2-start-schedule" {
  
    name = "EC2-Start-Schedule-${var.instance_id}"
    description = "Schedule to start EC2 instance."
    schedule_expression = "cron(${var.start_time})"

}


resource "aws_cloudwatch_event_target" "EC2-start-target" {
  
    rule = aws_cloudwatch_event_rule.EC2-start-schedule.name
    target_id = "start-lambda"
    arn = aws_lambda_function.EC2_toggler.arn

    input = jsonencode({
        "action" : "start"
    })

}


resource "aws_cloudwatch_event_rule" "EC2-stop-schedule" {
  
    name = "EC2-Stop-Schedule-${var.instance_id}"
    description = "Schedule to stop EC2 instance."
    schedule_expression = "cron(${var.stop_time})"

}


resource "aws_cloudwatch_event_target" "EC2-stop-target" {
  
    rule = aws_cloudwatch_event_rule.EC2-stop-schedule.name
    target_id = "stop-lambda"
    arn = aws_lambda_function.EC2_toggler.arn

    input = jsonencode({
        "action" : "stop"
    })

}


### Lambda Function Permission

resource "aws_lambda_permission" "allow-start" {
  
    statement_id = "AllowExecutionFromCloudWatchStart"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.EC2_toggler.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.EC2-start-schedule.arn

}


resource "aws_lambda_permission" "allow-stop" {
  
    statement_id = "AllowExecutionFromCloudWatchStop"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.EC2_toggler.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.EC2-stop-schedule.arn

}