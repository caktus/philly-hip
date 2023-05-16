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
inv utils.get-db-backup
```

## Monitoring

Amazon CloudWatch Metrics receives data via the [aws-cloudwatch-metrics](https://github.com/aws/eks-charts/tree/master/stable/aws-cloudwatch-metrics)
Helm chart. To view metrics, login to the AWS account (via the Caktus AssumeRole, above), then:

- Go to CloudWatch
- Click "All Metrics"
- Click "ContainerInsights"
- Drill down as needed

Alerts can be created based on the metrics if needed, e.g., to provide an alert on high CPU utilization.

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


## Error Logs

All Kubernetes cluster and application logs are sent to AWS CloudWatch, but it can be
useful to know when an error is logged. Specifically, as a part of maintaining the
project, certain developers are notified when an error is logged:

 - a log filter has been set up to catch all logs that contain the string "ERROR". You
   can find this filter in the AWS Console, in the CloudWatch service, by clicking on "Log
   groups", choosing the "/aws/eks/fluentbit-cloudwatch/logs" log group, and clicking on the
   "Metric filters" tab.
 - a CloudWatch alarm has been set up to watch the error filter. If an error gets caught
   by the filter, then the alarm is triggered, and posts to a Simple Notification Service
   (SNS) topic named "HIP_Errors_CloudWatch_Alarms_Topic"
 - the SNS topic emails the Caktus HIP development team (hip-philly-team@caktusgroup.com)
   that the alarm has been triggered due to an error on the site.

You may also view error logs in the AWS Console:
 - log in to the AWS Console
 - switch to the [HIP role](https://signin.aws.amazon.com/switchrole?roleName=CaktusAccountAccessRole-Admins&account=061553509755&displayName=Philly-PDPH)
 - navigate to the AWS CloudWatch service, and go to the "/aws/eks/fluentbit-cloudwatch/logs" log group

To watch for error logs in the terminal using `awslogs`:

```sh
awslogs get /aws/eks/fluentbit-cloudwatch/logs -GS --query log --watch | grep "ERROR"
```


### Receiving A Notification Of An Error

The "HIP_Errors_CloudWatch_Alarms_Topic" emails that notify developers that the alarm has been
triggered are pretty vague, with a subject like "ALARM: "HIP Errors alarm"", and a body
that begins with something like
"You are receiving this email because your Amazon CloudWatch Alarm ... has entered the ALARM
state". When receiving this alarm, it will be helpful to figure out more information about
the error, such as which environment (staging or production) the error occurred in and
how serious the error was. To do so,
 - click on the link in the email, which should take you to the AWS CloudWatch alarm (you
   will need to log into the AWS Console). Note the time that the alarm was first triggered.
 - you can then go to the CloudWatch logs and view the logs in the
   "/aws/eks/fluentbit-cloudwatch/logs" log group. You can click on the logs for a
   specific container, or search for specific terms, like "ERROR".

Alternately, you can check the errors using the command line. For example, to see all
logs from the past 3 hours that match "ERROR":

```sh
awslogs get /aws/eks/fluentbit-cloudwatch/logs -GS --query log --start='3h' | grep ERROR
```


## Production backup and hosting services configuration

[caktus.k8s-hosting-services](https://github.com/caktus/ansible-role-k8s-hosting-services)
manages database backups.

Run this command to set up database backups and monitoring services:

```sh
inv deploy.playbook -n deploy-hosting-services.yml
```
