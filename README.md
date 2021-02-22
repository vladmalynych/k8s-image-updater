# k8s-image-updater

### Description:
This application lists DockerHub tags, and compares them to currently deployed tags of k8s deployments.
In case if new image exists, k8s deployment image will be updated and notification will be sent to Slack `#dev-release` channel.

### Working hours
CronJob is executed in a predefined time window:
 - `[Mon - Fri] [09:00 - 18:00] [every 20 min]`

`Note:` in CronJob manifest, time is set according to a UTC timezone.
(All CronJob `schedule:` times are based on the timezone of the kube-controller-manager, on our prod it is set to UTC)

### Application configuration
This chapter describes how to add a new deployment to be automatically updated, to application.

Prerequisites:
 - Your GitHub repo should have setup automatic builds to DockerHub.
 - Each build should have unique tag (e.g `latest` - wrong / `123` - ok / `master-123` - ok)
 - DockerHub repo should have read permissions for readonly group.

Configuration:
 - To add new deployment simply add new `DeploymentResource` to `updater/settings/conf.py` `DEPLOYMENTS` list.
e.g.
```python
     DeploymentResource(organization="vladmalynych",    # DockerHub organization
                       repository="test",               # DockerHub repository
                       tag_regex="^([0-9]+)$",          # Dockerhub tag regex (should filter tags)
                       deploy_name="test",              # K8S deployment name
                       namespace="default"),            # K8S deployment namespace
```

`Note:` Dockerhub tag regex should specify group(1) with the unique build number, so that tags could be compared.
