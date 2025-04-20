import boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': 'my-video-data-bucket', 'Name': 'frame.jpg'}},
        MaxLabels=10
    )
    
    for label in response['Labels']:
        if label['Name'] in ['Knife', 'Scissors', 'Violence']:
            # Trigger CloudWatch alarm or SNS notification
            print(f"Alert: {label['Name']} detected with confidence {label['Confidence']}")
