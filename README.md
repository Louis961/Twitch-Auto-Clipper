<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--   <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Twitch Clip Generator</h3>

  <p align="center">
    Upload a Twitch log.txt viewer chat file from a recent stream to generate a peak activity clip timestamp range.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
<!--     <li><a href="#roadmap">Roadmap</a></li>
<!--     <li><a href="#contributing">Contributing</a></li> -->
<!--    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This project allows a user to uplaoad a log of their Twitch chat and recieve times stamps of a potential clip. This project
is written mostly in Python and has a HTML frontend.  It utilises AWS services such as Cognito, Amplify, S3 Buckets, Lambda, DynamoDB, IAM, and Amazon API Gateways(Restful APIs).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [AWS Amplify](https://aws.amazon.com/amplify/)
* [API Gateway](https://aws.amazon.com/api-gateway/)
* [Amazon Cognito](https://aws.amazon.com/cognito/)
* [Amazon S3](https://aws.amazon.com/s3/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
1. Download the repository and full read the READ.me

2. Enable AWS CloudWatch for the various services as it will make it a lot easier to monitor any function run by Lambda

### Prerequisites
* AWS User Account

### Installation
1. Create an IAM role for the following services to communicate and write: S3, Cloudwatch, 
   DynamoDB, Lambda, Amazon API Gateway
   [a] In a case if there are more than one users accessing the account create IAM group for the users

NOTE: Each addition of an AWS services will require an IAM role in order for the services to communicate with eachother

2. Initialize an S3 bucket instance and configure it to be public
   [a] Bucket policy
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::text-file/*"
        }
    ]
    }
    [b]Cross-origin resource sharing(CORS)
    [
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "POST",
            "GET",
            "PUT",
            "DELETE",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
    ]

3. Initialize DynamoDB table

4. Create a Lambda function for s3-trigger.py and configure the IAM role
   [a] Manual add trigger to the designated S3 bucket

5. Create a Cognito role
   [a] Click manage identity pool

   [b] Name the identiy pool and make sure that unauthenticated identities is enabled

   [c] After creating the identity pool modify the new created unauthenticated IAM role
   <pre>
        <code>
            {
            "Version": "2012-10-17",
            "Statement": [
            {
            "Sid": "PeakFinderAccess",
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "arn:aws:dynamodb:[Server]:[ACCOUNTID]:table/[TableName]"
            }
            ]
            } 
        </code>
   </pre>
   
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PeakFinderAccess",
            "Effect": "Allow",
            "Action": "dynamodb:*",
            "Resource": "arn:aws:dynamodb:[Server]:[ACCOUNTID]:table/[TableName]"
        }
    ]
    } 

6. Create an additional Lambda function for accessDDBTable.py 
   [a] Add an API gateway trigger 

7. Create an API gateway 
   [a] Create a method 

   [b] Create a GET resource 

   [c] Deploy the API 

8. Create a Amplify application
   [a] Modify the html with the approiate values

   [b] Zip the html by itself and uplaod to Amplify 

<p align="right">(<a href="#top">back to top</a>)</p>
