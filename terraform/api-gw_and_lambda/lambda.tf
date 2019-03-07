<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:3edd80a3a432216d1c49257069c8a946f36e6d078f1436e6c644e762b672f912
size 2685
=======
provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "example" {
  function_name = "ServerlessExample"

  s3_bucket = "blue-pigeons"
  s3_key = "v.1.0.0/example"

  handler = "main.handler"
  runtime = "nodejs6.10"

  role = "${aws_iam_role.lambda_exec.arn}"
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_example_lambda"
  
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17"
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

>>>>>>> e9ce1554c7cb8ee68498265c8f28104c05af85a3
