from flask import Flask, request, jsonify
import boto3
import os
from flask_cors import CORS
CORS(app)

app = Flask(__name__)

# Initialize AWS clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# S3 bucket name
BUCKET_NAME = 'my-video-data-bucket'

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Upload the file to S3
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Here you would call the Rekognition API or trigger the Lambda function
    # For example, you can analyze a specific image in S3
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': 'frame.jpg'}},
        MaxLabels=10
    )
    
    detected_labels = [label['Name'] for label in response['Labels']]
    return jsonify({"detected_labels": detected_labels}), 200

if __name__ == '__main__':
    app.run(debug=True)