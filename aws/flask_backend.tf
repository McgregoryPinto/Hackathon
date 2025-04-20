resource "aws_lambda_function" "flask_backend" {
  function_name = "FlaskBackend"
  handler = "app.lambda_handler"
  runtime = "python3.8"
  role = aws_iam_role.lambda_exec.arn
  filename = "lambda_function_payload.zip" // Your zipped Flask application code

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.video_bucket.bucket
    }
  }
}

resource "aws_api_gateway_rest_api" "flask_api" {
  name        = "FlaskAPI"
  description = "API for Flask backend"
}

resource "aws_api_gateway_resource" "upload_resource" {
  rest_api_id = aws_api_gateway_rest_api.flask_api.id
  parent_id   = aws_api_gateway_rest_api.flask_api.root_resource_id
  path_part   = "upload"
}

resource "aws_api_gateway_method" "upload_method" {
  rest_api_id   = aws_api_gateway_rest_api.flask_api.id
  resource_id   = aws_api_gateway_resource.upload_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.flask_backend.function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_api_gateway_integration" "upload_integration" {
  rest_api_id = aws_api_gateway_rest_api.flask_api.id
  resource_id = aws_api_gateway_resource.upload_resource.id
  http_method = aws_api_gateway_method.upload_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.flask_backend.invoke_arn
}
