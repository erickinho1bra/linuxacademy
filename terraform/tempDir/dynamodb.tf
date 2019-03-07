provider "aws" {
  region = "us-east-1"
  profile = "xelima"
}

resource "aws_dynamodb_table" "ellen_royalty_dev_artist" {
}

resource "aws_s3_bucket" "ellen-royalty-dev-qa" {
}
