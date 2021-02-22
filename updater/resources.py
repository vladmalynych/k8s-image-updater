class DeploymentResource:
    def __init__(self, organization: str, repository: str, tag_regex: str, deploy_name: str, namespace: str):
        self.organization = organization
        self.repository = repository
        self.tag_regex = tag_regex
        self.deploy_name = deploy_name
        self.namespace = namespace
