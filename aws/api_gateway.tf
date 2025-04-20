provider "aws" {
  region = "us-east-1"
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

// SNS Topic
resource "aws_sns_topic" "alerts" {
  name = "ObjectDetectionAlerts"
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

// S3 Bucket for Video Storage
resource "aws_s3_bucket" "video_bucket" {
  bucket = "my-video-data-bucket"
  acl    = "private"
}
