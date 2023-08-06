terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data"
    key     = "terraform/ecs-cluster/skitai-novpc/task-def/ecsdep/terraform.tfstate"
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

# variables -----------------------------------------------
variable "awslog_region" {
  default = "ap-northeast-1"
}

variable "stages" {
  default = {
    default = {
        env_service_stage = "production"
        hosts = ["skitai.sns.co.kr"]
        listener_priority = 10
        service_name = "ecsdep"
        task_definition_name = "ecsdep"
    }
    qa = {
        env_service_stage = "qa"
        hosts = ["skitai-qa.sns.co.kr"]
        listener_priority = 11
        service_name = "ecsdep--qa"
        task_definition_name = "ecsdep--qa"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    desired = 1
    min = 1
    max = 4
    cpu = 100
    memory = 80
  }
}

variable "exposed_container" {
  default = [{
    name = "skitai-nginx"
    port = 80
  }]
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/ping"
        matcher = "200,301,302,404"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
    }
  }
}

variable "loggings" {
  default = ["skitai-app", "skitai-nginx"]
}

variable "loadbalancing_pathes" {
  default = ["/*"]
}

variable "requires_compatibilities" {
  default = ["EC2"]
}

variable "service_resources" {
  default = {
    memory = 160
    cpu = 512
  }
}

variable "vpc_name" {
  default = ""
}