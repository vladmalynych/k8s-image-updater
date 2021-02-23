import re
import logging

from updater.api.dockerhub import DockerHub
from updater.api.kube import Kube
from updater.settings.conf import DEPLOYMENTS
from updater.settings.settings import SLACK_HOOK, SLACK_NOTIFICATION_CHANNEL
from updater.api.slack import send_notification
LOG = logging.getLogger(__name__)


def parse_docker_image(docker_image: str) -> dict:
    """
    Parse image url (gets image parts: {full, docker_repo, docker_tag, branch, buildno})
    """
    parsed_image = re.search(r'(.+)/(.+):(.+)', docker_image)
    return {
        'full': parsed_image.group(0),
        'organization': parsed_image.group(1),
        'repo': parsed_image.group(2),
        'tag': parsed_image.group(3),
    }


def get_docker_build(docker_tag: str, tag_regex: str):
    return int(re.search(r'{}'.format(tag_regex), docker_tag).group(1))


def main():
    log_level = logging.INFO
    logging.basicConfig(format='%(asctime)s,%(msecs)03d - %(message)s', level=log_level, datefmt='%H:%M:%S')
    logging.getLogger('kubernetes').setLevel(logging.INFO)

    for DEPLOYMENT in DEPLOYMENTS:
        LOG.info(f"{DEPLOYMENT.deploy_name} :")
        dockerhub_image = parse_docker_image(DockerHub(DEPLOYMENT).get_latest_image())
        if not dockerhub_image:
            LOG.error(f"No images available for {DEPLOYMENT.deploy_name}")
            continue
        LOG.info(f"Latest DockerHub image found [{dockerhub_image['full']}]")
        dockerhub_image_num = get_docker_build(dockerhub_image['tag'], DEPLOYMENT.tag_regex)


        kube = Kube(DEPLOYMENT)
        deployment = kube.get_deployment()
        kube_image = parse_docker_image(deployment.spec.template.spec.containers[0].image)
        LOG.info(f"Current deployment image found [{kube_image['full']}]")
        kube_image_num = get_docker_build(kube_image['tag'], DEPLOYMENT.tag_regex)

        if dockerhub_image_num > kube_image_num:
            LOG.info(f"Newer image available: [{dockerhub_image_num} > {kube_image_num}]")
            deployment.spec.template.spec.containers[0].image = dockerhub_image['full']
            kube.patch_deployment(deployment)
            if not SLACK_HOOK or not SLACK_NOTIFICATION_CHANNEL:
                LOG.info(f"Slack is not configured, skipping notification...")
            else:
                send_notification(title=f"Released: [{DEPLOYMENT.deploy_name} - {dockerhub_image['tag']}] :tada:",
                                  color="good",
                                  text=f":gear: {DEPLOYMENT.deploy_name}\n"
                                       f"Previous image: `{kube_image['full']}`\n"
                                       f"Deployed image: `{dockerhub_image['full']}`",
                                  footer="")
        else:
            LOG.info(f"Nothing to deploy: [{dockerhub_image_num} <= {kube_image_num}]")


if __name__ == '__main__':
    main()
