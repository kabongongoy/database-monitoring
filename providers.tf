terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


provider "aws" {
  region = "ap-southeast-2"
  
  default_tags {
    tags = {
      Service     = "RDS"
      Project     = "Database-Monitoring"
      Environment = "dev"
      Department  = "Technology"
      Team        = "DevOps"
      Country     = "Australia"
      TICKET      = "SCAL-2890"
      Terraform_Module_Path = "modules/rds"
      TF_Module  = "rds-monitoring"
      TF_Module_Repo_URL = "url"
      Managed_By = "Terraform"
    }
  }
}



# terraform {
#   required_version = ">= 1.0.0"

#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 4.0"
#     }
#   }
#   backend "s3" {
#     bucket         = "cns-s3-bkt-terraform-state-storage"
#     encrypt        = true
#     dynamodb_table = "cns-dyn-db-table-tf-state-locking-syd"
#     key            = "accounts/cns-dev/networking/main.tfstate"
#     region         = "ap-southeast-2"
#     assume_role = {
#       role_arn = "arn:aws:iam::449417798447:role/cns-iam-role-terraform-state-access"
#     }
#   }
# }



# provider "aws" {
#   region = "ap-southeast-2"
  
#   default_tags {
#     tags = {
#       Service     = "VPC"
#       Project     = "AWS-Networking"
#       Environment = "dev"
#       Department  = "Technology"
#       Team        = "DevOps"
#       Country     = "Australia"
#       TICKET      = "SCAL-2890"
#     }
#   }
# }
