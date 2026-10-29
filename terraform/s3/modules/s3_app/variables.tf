variable "bucket" {
  description = "Bucket name"
  type        = string
}

variable "config" {
  description = "App configuration from YAML"
  type        = any
}

locals {
  acl           = lookup(var.config, "acl", "private")
  versioning    = lookup(var.config, "versioning", false)
  force_destroy = lookup(var.config, "force_destroy", false)
  quota_gib     = lookup(var.config, "quota_gib", 0)

  lifecycle_rules = lookup(var.config, "lifecycle_rules", [])
  cors_rules      = lookup(var.config, "cors_rules", [])

  policy = lookup(var.config, "policy", {})
  bucket_actions = distinct(concat([
    "s3:GetBucketLocation",
    "s3:ListBucket",
    "s3:ListBucketMultipartUploads",
  ], lookup(local.policy, "bucket_actions", [])))
  object_actions = distinct(concat([
    "s3:GetObject",
    "s3:PutObject",
    "s3:DeleteObject",
    "s3:AbortMultipartUpload",
    "s3:ListMultipartUploadParts",
  ], lookup(local.policy, "object_actions", [])))
}
