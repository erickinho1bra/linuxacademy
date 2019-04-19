provider "aws" {
  region  = "${var.aws_region}"
  profile = "${var.aws_profile}"
}

resource "aws_security_group" "cloudfront_g" {
  name = "cloudfront_g"
  description = "security group that is autoupdated with appropriate ingress rules for IPs belonging to the GLOBAL edge locations"
}

resource "aws_security_group" "cloudfront_r" {
  name = "cloudfront_r"
  description = "security group that is autoupdated with appropriate ingress rules for IPs belonging to the REGIONAL edge locations"
}


resource "aws_iam_instance_profile" "sGUpdate" {
  name = "sGUpdate"
  role = "${aws_iam_role.sGUpdate.name}"
}

resource "aws_iam_role_policy" "sGUpdate" {
  name = "sGUpdate"
  role = "${aws_iam_role.sGUpdate.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroups",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role" "sGUpdate" {
  name = "sGUpdate"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
  {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
  },
      "Effect": "Allow",
      "Sid": ""
      }
    ]
}
EOF
}

resource "aws_lambda_function" "sGUpdate" {
  filename      = "function.zip"
  function_name = "updateSGAWS"
  role          = "${aws_iam_role.sGUpdate.arn}"
  handler       = "updateSGAWS.lambda_handler"

  source_code_hash = "${filebase64sha256("function.zip")}"
  runtime          = "python2.7"
  timeout          = 15
}

resource "aws_sns_topic" "sGUpdate" {
  name = "sGUpdate"
}

resource "aws_sns_topic_subscription" "sGUpdate" {
  topic_arn = "${aws_sns_topic.sGUpdate.arn}"
  protocol = "lambda"
  endpoint = "${aws_lambda_function.sGUpdate.arn}"
}

resource "aws_lambda_permission" "sGUpdate" {
  statement_id = "sNSToTriggerLambda"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.sGUpdate.function_name}"
  principal = "sns.amazonaws.com"
  source_arn = "${aws_sns_topic.sGUpdate.arn}"
}

