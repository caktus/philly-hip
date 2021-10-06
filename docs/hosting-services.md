# Hosting Services

The services configured for this project are:
* PostgreSQL database backups to S3 (within HIP AWS account)
* Cloudwatch logging (within HIP AWS account)


## Production database disaster recovery

In the event a restore from a historical backup is needed, access to the [Caktus
AssumeRole is
required](https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md#aws-accounts).
Once you have that access, you can use invoke tools to pull historical backups.

To download the latest `daily` backup:

```sh
inv utils.get-db-backup --profile philly-hip
```

## Logging

Amazon CloudWatch Logs aggregates Kubernetes cluster and application logs. You
can view the logs in the AWS Console or using `awslogs`.

View all logs:

```sh
awslogs get /aws/eks/fluentbit-cloudwatch/logs -G --query log --watch
```

Example to view only app pod logs:

```sh
awslogs get /aws/eks/fluentbit-cloudwatch/logs "fluentbit-kube.var.log.containers.app*" -GS --query log --watch
```


## Production backup and hosting services configuration

[caktus.k8s-hosting-services](https://github.com/caktus/ansible-role-k8s-hosting-services)
manages database backups.

Run this command to set up database backups and monitoring services:

```sh
inv deploy.playbook -n deploy-hosting-services.yml
```
