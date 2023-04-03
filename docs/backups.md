# Managed Hosting Services

Caktus provides managed hosting services for this project. Please see [Disaster
Recovery](https://caktus.github.io/developer-documentation/reference/disaster-recovery/)
for more information.

The services configured for this project are:
* **PostgreSQL database backups:** Backups are stored in the `hip-production-philly-backups` (us-east-2) S3 bucket.
* **Uploaded media backups:** S3 objects are replicated from `hip-production-philly-private-assets` (us-east-1) to `hip-dr-philly-private-assets` (us-east-2). 

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