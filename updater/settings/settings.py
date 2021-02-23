import os

# Slack settings (optional)
SLACK_NOTIFICATION_CHANNEL = os.getenv('SLACK_NOTIFICATION_CHANNEL', None)
SLACK_HOOK = os.getenv('SLACK_HOOK', None)

# DockerHub settings
DOCKER_HUB_USER = str(os.getenv('DOCKER_HUB_USER'))
DOCKER_HUB_PASSWORD = str(os.getenv('DOCKER_HUB_PASSWORD'))
DOCKER_HUB_AUTH_DOMAIN = "auth.docker.io"
DOCKER_HUB_AUTH_SERVICE = "registry.docker.io"
DOCKER_HUB_API_DOMAIN = "registry-1.docker.io"
