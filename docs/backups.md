# Managed Hosting Services

Caktus provides managed hosting services for this project. Please see [Disaster
Recovery](https://caktus.github.io/developer-documentation/reference/disaster-recovery/)
for more information.

The services configured for this project are:
* **PostgreSQL database backups:** Backups are stored in the `hip-production-assets` (us-east-2) S3 bucket.
* **Uploaded media backups:** S3 objects are replicated from `hip-production-philly-assets` (us-east-1) to `hip-dr-assets` (us-east-2).

## Backup Verification Procedures

Please follow the workflow outlined in [Disaster
Recovery](https://caktus.github.io/developer-documentation/reference/disaster-recovery/).

Additional documentation for backup verifications can be found here: [Backups: Kubernetes Backups](https://docs.google.com/document/d/16ke-22G1m04la-9X2kuR_QKSvXrnNXAx-pr5VTuBRgE/edit#)


## Production backup configuration

[caktus.k8s-hosting-services](https://github.com/caktus/ansible-role-k8s-hosting-services)
manages database backups. Database backups are in the `hip-production-philly-backups` S3 bucket.

Run this command to set up database backups:

```sh
inv deploy.install
inv production deploy.playbook -n deploy-hosting-services.yml
```

To test a cronjob, run:

```
kubectl create job -n hip-hosting-services --from=cronjob/backup-job-daily daily-test-01
```