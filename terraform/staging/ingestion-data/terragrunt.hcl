include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_repo_root()}//modules"
}

locals {
  project_id = read_terragrunt_config(find_in_parent_folders("env.hcl")).inputs.project_id
}

inputs = {
  iam_config = {
    project_id = local.project_id
  }
}