import re
import logging

from updater.requests import send_request
from updater.settings import settings
from updater.settings.conf import DeploymentResource

LOG = logging.getLogger(__name__)


class DockerHub:
    def __init__(self, deployment_res: DeploymentResource):
        self.deployment_res = deployment_res
        self.auth_scope = f"repository:{self.deployment_res.organization}/{self.deployment_res.repository}:pull"
        # Get token for scope
        self.token = self._get_token()

    def _get_token(self):
        url = f"https://{settings.DOCKER_HUB_AUTH_DOMAIN}/token?service={settings.DOCKER_HUB_AUTH_SERVICE}&scope={self.auth_scope}"
        auth = (settings.DOCKER_HUB_USER, settings.DOCKER_HUB_PASSWORD)
        response = send_request(method='GET', url=url, payload="", headers="", auth=auth)
        LOG.info(f'Token generated: {response.status_code}')
        return response.json()['token']

    def get_tags(self):
        url = f"https://{settings.DOCKER_HUB_API_DOMAIN}/v2/{self.deployment_res.organization}/{self.deployment_res.repository}/tags/list"
        headers = {"Authorization": "Bearer {}".format(self.token)}
        response = send_request(method='GET', url=url, payload="", headers=headers, auth="")
        LOG.info(f'Tags listed: {response.status_code}')
        return response.json()['tags']

    def get_latest_tag(self):
        tags = self.get_tags()
        if not tags:
            LOG.info(f"Tags not found in {self.deployment_res.repository}")
            return None
        filter_regex = re.compile(r'{}'.format(self.deployment_res.tag_regex))
        matching_tags = [(tag.group(0), int(tag.group(1))) for tag in (filter_regex.match(tag_raw) for tag_raw in tags) if tag]
        if not matching_tags:
            LOG.info(f"No matching tags found in {self.deployment_res.repository}")
            return None
        max_tag = max(matching_tags, key=lambda tag: tag[1])
        return max_tag[0]

    def get_latest_image(self):
        latest_tag = self.get_latest_tag()
        if not latest_tag:
            return None
        return f"{self.deployment_res.organization}/{self.deployment_res.repository}:{latest_tag}"
