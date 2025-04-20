provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "rekognition_handler" {
  filename         = "lambda_function_payload.zip" // Your zipped Lambda function code
  function_name    = "rekognitionHandler"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_recognition.lambda_handler"
  runtime          = "python3.8"

  environment {
    variables = {
      REKOGNITION_BUCKET = aws_s3_bucket.video_bucket.bucket
    }
  }
}

resource "aws_s3_bucket" "video_bucket" {
  bucket = "my-video-data-bucket"
  acl    = "private"
}

resource "aws_cloudwatch_metric_alarm" "object_detected_alarm" {
  alarm_name          = "ObjectDetectedAlarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ObjectDetected"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}

resource "aws_sns_topic" "alerts" {
  name = "ObjectDetectionAlerts"
}

// API Gateway
resource "aws_api_gateway_rest_api" "my_api" {
  name        = "MyAPI"
  description = "API for video streaming and alarms"
}

// WebSocket API
resource "aws_apigatewayv2_api" "websocket_api" {
  name          = "WebSocketAPI"
  protocol_type = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

// IAM Role for API Gateway
resource "aws_iam_role" "api_gateway_role" {
  name = "api_gateway_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })
}
