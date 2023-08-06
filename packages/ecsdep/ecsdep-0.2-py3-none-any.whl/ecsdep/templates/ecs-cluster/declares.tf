terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data"
    key     = "terraform/ecs-cluster/skitai-novpc/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-1"
}

variable "template_version" {
  default = "1.1"
}

variable "cluster_name" {
  default = "skitai-novpc"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "ami" {
  default = "amzn2-ami-ecs-hvm-*-x86_64-*"
}

variable "cors_hosts" {
  default = []
}

variable "cert_name" {
  default = "sns.co.kr"
}

variable "public_key_file" {
  default = "/app/libs/ecsdep/dep/ecsdep.pub"
}

variable "autoscale" {
  default = {
    desired = 1
    min = 1
    max = 4
    cpu = 50
    memory = 50
  }
}

variable "az_count" {
  default = 3
}

variable "vpc" {
  default = {
    cidr_block = ""
    octet3s = [10, 20, 30]
  }
}