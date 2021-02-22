import logging

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from updater.settings.conf import DeploymentResource

LOG = logging.getLogger(__name__)


class Kube:
    def __init__(self, deployment_res: DeploymentResource):
        self.deployment_res = deployment_res
        # Load kube config
        config.load_incluster_config()
        self.apps_v1 = client.AppsV1Api()

    def get_deployment(self):
        try:
            LOG.info(f"Reading deployment {self.deployment_res.deploy_name}")
            return self.apps_v1.read_namespaced_deployment(name=self.deployment_res.deploy_name,
                                                           namespace=self.deployment_res.namespace)
        except ApiException as e:
            LOG.error("Exception when trying read_namespaced_deployment: {}\n".format(e))
            raise

    def patch_deployment(self, body):
        try:
            self.apps_v1.patch_namespaced_deployment(name=self.deployment_res.deploy_name,
                                                     namespace=self.deployment_res.namespace,
                                                     body=body)
            LOG.info(f"Patched deployment {self.deployment_res.deploy_name}")
        except ApiException as e:
            LOG.error("Exception when trying patch_namespaced_deployment: {}\n".format(e))
            raise
