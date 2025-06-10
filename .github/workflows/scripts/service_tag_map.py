"""
Mapping of service identifiers to their corresponding Docker image environment variable names.

Keys:
    - "openedx": Open edX platform container
    - "mfe": Micro-frontend container
    - "aspects-superset": Superset-based reporting container

Values:
    Environment variable names used to specify Docker images for each service.
"""
service_tag_map = {
  "openedx": "DOCKER_IMAGE_OPENEDX",
  "mfe": "MFE_DOCKER_IMAGE",
  "aspects-superset": "DOCKER_IMAGE_SUPERSET"
}
