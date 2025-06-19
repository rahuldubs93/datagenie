terraform {
  backend "s3" {
  
} 
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.66.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
  profile = var.profile
  default_tags {
    tags = {
      terraform_source_url = "https://git.ds.corp.zoom.us/zoom-data-team/data-platform-architecture/services/zdt_datagenie.git"
      team                 = "zoom_data_team"
      owner                = "saurabh.srivastava@zoom.us skanda.ganapathy@zoom.us"
    }
  }

}