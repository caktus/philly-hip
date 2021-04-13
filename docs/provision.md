# Provisioning

Historical note. Initial development on this project was done using a staging server in
the Caktus Saguaro cluster. As of April 2021, both staging and production have been
provisioned in the City of Philadelphia's AWS subaccount (ID: 061553509755)

This document explains the steps we took to provision these environments. They DO NOT
need to be run again, unless we are re-provisioning them. If you are looking for
documentation on how to deploy updates to the project, look at [deploy.md](deploy.md).
The secrets that are mentioned below are all encrypted in the repo, but a copy has also
been placed in the LastPass entry, "PDPH Philly HIP Secrets" (folder: "Shared-PDPH")


## Get AssumeRole access

Using the IAM User account provided by PDPH, we created an IAM Role which delegates
access to our Caktus AWS account so that all approved users of our Caktus account will
have AdministratorAccess in the PDPH subaccount. The Role ARN is:
`arn:aws:iam::061553509755:role/CaktusAccountAccessRole-Admins`

## AWS CLI access

We followed the [Assume Role
instructions](https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md#aws-accounts)
to set up our awscli account. We will use `philly-hip` for our AWS profile name.

Test that it works:

```sh
(hip)$ export AWS_PROFILE=philly-hip
(hip)$ aws s3 ls
2021-03-17 15:42:16 aws-cloudtrail-logs-061553509755-2af21f3a
2021-03-18 10:47:34 cf-templates-1798dkeaoydk0-us-east-1
...
```

We updated our local environment variable to use this new `AWS_PROFILE`. The remaining
steps in this document assume that you are using this `AWS_PROFILE`.

## Create a vault password

1. We generated a long password and saved it to AWS with this command:

    ```sh
    (hip)$ aws secretsmanager create-secret --name hip-ansible-vault-password --secret-string <long-secret>
    {
        "ARN": "arn:aws:secretsmanager:us-east-1:061553509755:secret:hip-ansible-vault-password-JYhbao",
        "Name": "hip-ansible-vault-password",
        "VersionId": "0aa88786-7385-4bf1-abb6-b184cbcbfe95"
    }
    ```

2. We recorded the ARN that is returned, which we'll need for setting up CI later.

## Set up AWS Web Stacks

We obtained the [latest release of the
aws-web-stacks](https://github.com/caktus/aws-web-stacks/releases). This is a zip file.
We extracted the `eks-no-nat.yml` file and placed it in `/deploy/stack/`

We then ran the CloudFormation set up playbook:

```sh
(hip)$ inv deploy.playbook deploy-cf-stack.yml
```

## Set up the cluster

We followed the instructions at https://github.com/caktus/ansible-role-k8s-web-cluster.

Make sure you have [helm installed](https://helm.sh/docs/intro/install/).

Update your ~/.kube/config with the new cluster's context:

```sh
(hip)$ aws eks update-kubeconfig --name=philly-hip-stack-cluster
Added new context arn:aws:eks:us-east-1:061553509755:cluster/philly-hip-stack-cluster to /home/vkurup/.kube/config
```

We set `k8s_context` to that ARN.

Once that is all set, run the playbook:

```sh
(hip)$ inv deploy.playbook deploy-cluster.yml
```

This ran without errors, but there was no load balancer. See
https://github.com/caktus/ansible-role-k8s-web-cluster/issues/23 for solutions to this
issue.

## Set up the docker registry

AWS web stacks creates a docker registry for us. We just need to find out about it and
put the details in our configuration files.

1. Find the URL for the docker registry:

   ```sh
   (hip)$ aws ecr describe-repositories
   ...
     "repositoryUri": "061553509755.dkr.ecr.us-east-1.amazonaws.com/philly-hip-stack-applicationrepository-kk92mehevd86",
   ...
   ```

2. Add the `repositoryUri` value from the output above to `tasks.py` as the value for
   `repository` in the `ns.configure()` command at the bottom of the file.

3. Test it out:

    ```sh
    (hip)$ inv aws.docker-login
    (hip)$ inv image.push
    ```

4. Check to be sure the image was pushed:

    ```sh
    (hip)$ aws ecr list-images --repository-name philly-hip-stack-applicationrepository-kk92mehevd86
    ... successful output listing an image ...
    ```

## Get access to the cluster

1. Update `tasks.py` and set `cluster` to `philly-hip-stack-cluster` in the
   `ns.configure()` command at the bottom of the file.

2. Get access to the cluster so you can run `kubectl` locally:

    ```sh
    (hip)$ inv aws.configure-eks-kubeconfig
    ...
    ```

## Create a DB on the RDS instance

1. Get the RDS params you'll need:

    ```sh
    (hip)$ aws rds describe-db-instances
    ```

   * From that output, get `MasterUsername`, `DBName`, and `Endpoint.Address`.
   * Get the `MasterPassword` from the LastPass entry, "PDPH Philly HIP Secrets".
   * Choose or generate a `HipDbPassword` that you'll use for HIP. Save that
     somewhere so that you can encrypt it later in the process.


2. Using those parameters, create the DB with the proper permissions. (Anything in curly
   brackets is meant to represent a placeholder for the actual values from the step above):

    ```sh
    (hip)$ inv pod.debian
    root@debian:/# apt update && apt install postgresql-client -y
    root@debian:/# psql postgres://{MasterUsername}:{MasterPassword}@{Endpoint.Address}:5432/{DBName}
    => CREATE DATABASE hip_staging;
    => CREATE ROLE hip_staging WITH LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION PASSWORD '{HipDbPassword}';
    => GRANT CONNECT ON DATABASE hip_staging TO hip_staging;
    => GRANT ALL PRIVILEGES ON DATABASE hip_staging TO hip_staging;
    ```

3. Once the DB is created, run a similar command to connect to it as the RDS superuser
   so that we can install the Postgresql citext extension:

   ```sh
    (hip)$ inv pod.debian
    root@debian:/# apt update && apt install postgresql-client -y
    root@debian:/# psql postgres://{MasterUsername}:{MasterPassword}@{Endpoint.Address}:5432/hip_staging
    => CREATE EXTENSION citext;
   ```

4. Repeat steps 2 and 3 to create a `hip_production` database with a different password.

### Point your desired domain at the load balancer

1. Find the load balancer URL:

    ```sh
    (hip)$ kubectl get svc -n ingress-nginx
    ```

2. Copy the `EXTERNAL-IP` value for the LoadBalancer from that output. It is the load balancer URL.

3. Go to Cloudflare and create a CNAME from your desired subdomain pointing to that URL.

    ```
    hip-staging.caktus-built.com -> a5708797ea2d24401910ac2608f0ba4e-2bd02263e9f15ea0.elb.us-east-1.amazonaws.com
    ```

4. Repeat step 3 to point `hip-prod.caktus-built.com` at the SAME load balancer URL. The
   load balancer will send requests to the proper environment based on the request
   domain.

### Create the k8s service account and get the secret API key

Follow the instructions in [the Django k8s
repo](https://github.com/caktus/ansible-role-django-k8s) to create the service account
that will do the deploys, and get the API key for that account. Here are the steps to
complete that process.

1. Run the deploy once. This will fail, but it will output the text value for the public
   certificate of the cluster, which you'll use in the next step.

   Note that the deploy command needs a `--tag` but we won't be deploying anything yet,
   so it doesn't matter what you provide.

   ```sh
   (hip)$ inv staging deploy --tag foo
   ```

2. Copy and paste the certificate output of the previous command into to the file
   `deploy/k8s_auth_ssl_ca_cert.txt`.

3. Make sure `k8s_auth_api_key` is set to `""` in `deploy/host_vars/staging.yml` and
   then run it again. This will again fail, but will give you a secret value for the
   `k8s_auth_api_key`.

   ```sh
   (hip)$ inv staging deploy --tag foo
   ```

4. Take the value from the error output of the previous command, encrypt it, and put the
   encrypted value in `deploy/host_vars/staging.yml` for `k8s_auth_api_key`.

     ```sh
     (hip)$ cd deploy
     (hip)$ ansible-vault encrypt_string <secret>
     ```

5. Repeat step 4 for the other secrets that we need in `host_vars/staging.yaml`
    * `HipDbPassword` from above as `database_password`.
    * Encrypt a long secret key and save it as
      `k8s_environment_variables/DJANGO_SECRET_KEY`.

6. Finally, once the staging environment is provisioned, repeat steps 3 through 5 for
   production.

### Set up email with Amazon SES

Follow these instructions to create a new SMTP user:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html

* IAM User Name: `ses-smtp-user.philly-hip`
* Copy the SMTP Username and SMTP Password and encrypt them to EMAIL_HOST_USER and
  EMAIL_HOST_PASSWORD respectively under the `k8s_environment_variables` heading in
  `deploy/host_vars/staging.yml`.

We use the same IAM User and creds for sending email on staging and production.

### Deploy!

1. Finally, do the deploy again, and it should work.

    ```sh
    (hip)$ inv staging image deploy
    ```

2. Confirm that you see pods running in our namespace.

    ```sh
    (hip)$ kubectl get pods --namespace=hip-staging
    NAME                         READY   STATUS    RESTARTS   AGE
    app-84f486b849-pfp7k         1/1     Running   0          5m
    app-84f486b849-zdjlz         1/1     Running   0          5m
    memcached-797d6b546c-fn862   1/1     Running   0          7m
    ```

### Create S3 buckets for media and assets

This role creates a private bucket for media, a public bucket for assets, and the
accompanying security roles so that all of the EKS nodes can properly access those
buckets. Note that at the time of provisioning, our settings are not using the static
assets bucket, but are instead storing files on each instance.

```sh
(hip)$ inv staging deploy.playbook deploy-s3.yml
```

This needs to be done once for each environment.

### Create a special IAM user for CI deploys

[Create the special IAM user for CI
deploys](https://github.com/caktus/ansible-role-django-k8s#amazon-iam-adding-a-limited-aws-iam-user-for-ci-deploys).

As detailed in the documentation in the previous link, you will need the SecretsManager
ARN that we saved above, and once the IAM user is created, you'll need to create AWS
credentials in the console and then copy/paste those to you Github Actions Secrets.

This only needs to be done once for the cluster. Github Actions will use the same IAM
user to deploy to both staging and production.
