# AWS-Textract-Based-Receipt-Processing-System

---
## Overview

 This project automates the extraction of structured data from unstructured receipts using AWS Textract. Users can upload receipts (e.g., .png, .jpg, .pdf) to an S3 bucket. A Lambda function is triggered, Textract processes the receipt, and a well-formatted summary email is sent to the user with extracted details like store address, date, time, item list, quantity, and prices.



---
## Architecture

![Image](https://github.com/user-attachments/assets/e12a55f8-0599-4c85-9e63-fa4a4b47c84c)


---
## Features

 *  Auto-triggered processing on S3 receipt upload
 *  OCR-based text extraction using AWS Textract
 *  Structured output formatting with receipt metadata and item list
 *  Polished HTML summary email sent via Amazon SES
 *  CloudWatch logging for transparency and debugging

 ---
## Tech Stack

* AWS S3 – For storing uploaded receipts

* AWS Lambda – Core orchestration and logic

* AWS Textract – Document text extraction from receipts

* AWS SES – Sending formatted receipt summaries

* AWS CloudWatch – Logging and monitoring

---
## Project Flow

 * User uploads a receipt image or PDF to receipt-collector-uploads bucket

 * Lambda is automatically triggered

 * Lambda uses Textract to extract structured fields:

   * Address

   * Date and Time

   * Transaction ID

   * Item names, quantities, prices

   * Lambda formats this into a clean HTML email

* The formatted receipt is emailed to the user via SES

  * Logs of the operation are written to CloudWatch

---
## Getting Started
 ###Prerequisites
  * AWS account with:

       * Amazon Textract access

       * SES verified sender email

       * Necessary Lambda permissions (Textract, SES, S3)

       * Configured S3 bucket: receipt-collector-uploads

---
## Setup Steps

  * Create an S3 bucket for uploads (receipt-collector-uploads)

  * Deploy the Lambda function with Textract & SES permissions

  * Verify the sender email in Amazon SES

  * Upload a receipt to trigger the pipeline and receive a formatted email

---
## Key Takeaways
 * Textract can extract structured data even from scanned/unstructured documents
 * Automating receipt processing simplifies expense tracking
 * Polished HTML email output improves readability and user experience
 * Serverless pipeline minimizes infrastructure overhead

---
## Future Enhancements
   * Store extracted data in DynamoDB or S3 for analytics

   * Support multi-page receipts

   * Add retry/failure notifications

   * Enable voice summary via Amazon Polly (for accessibility)

   * Add UI upload form via Amazon S3 Static Website or React + API Gateway

