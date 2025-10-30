variable "GITHUB_REF_NAME" {
  default = "latest"
}

variable "GITHUB_SHA" {
  default = "latest"
}

target "default" {
  context = "."
  args = {
    REVISION = "${GITHUB_SHA}"
  }
  dockerfile = "Dockerfile"
  tags = ["ghcr.io/semaforinformatik/intens-cloud-management-daemon:${GITHUB_REF_NAME}", "ghcr.io/semaforinformatik/intens-cloud-management-daemon:latest"]
  cache-from = ["type=gha,scope=config-controller"]
  cache-to = ["type=gha,mode=max,scope=config-controller"]
}

