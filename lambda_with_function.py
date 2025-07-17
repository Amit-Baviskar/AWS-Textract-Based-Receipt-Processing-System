import boto3
import json
import urllib.parse
import os
from datetime import datetime

# AWS clients
s3 = boto3.client('s3')
textract = boto3.client('textract')
ddb = boto3.resource('dynamodb')
ses = boto3.client("ses")

# Environment variables
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
verified_email = SENDER_EMAIL

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key_raw = event['Records'][0]['s3']['object']['key']
        key = urllib.parse.unquote_plus(key_raw)

        # Step 1: Extract text using Textract
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )

        # Step 2: Collect all lines
        lines = [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']
        full_text = "\n".join(lines)

        # Step 3: Save to DynamoDB
        parsed_data = {
            "ReceiptID": key,
            "RawText": full_text,
            "UploadTime": str(context.aws_request_id)
        }
        table = ddb.Table("ReceiptsTable")
        table.put_item(Item=parsed_data)

        # Step 4: Format email as a simple table-style plain text
        email_body = f"""Hi there,

✅ Your receipt has been successfully uploaded and processed.

Here's a preview of the extracted text:

------------------------------------------------------------
     Receipt Text 
------------------------------------------------------------
"""

        for i, line in enumerate(lines[:]):
            email_body += f"{i+1:>2}. {line}\n"

        email_body += """------------------------------------------------------------

This receipt was processed using AWS Textract.
If you need the full receipt text or have questions, contact support.

📁 Receipt ID: {}
🕒 Upload Request ID: {}

Thanks,
Your Receipt Processing System
""".format(key, context.aws_request_id)

        # Step 5: Send email
        ses.send_email(
            Source=verified_email,
            Destination={"ToAddresses": [verified_email]},
            Message={
                "Subject": {"Data": "🧾 Receipt Processed Successfully"},
                "Body": {
                    "Text": {"Data": email_body}
                }
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('✅ Receipt processed and emailed successfully.')
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
