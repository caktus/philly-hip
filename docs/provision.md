# Provisioning

Provisioning staging and production will be different since we will be using the Caktus
Saguaro cluster for staging (and it is already provisioned), but we will have to
provision the production cluster before we can use it. Once provisioned, the steps to
deploy to either staging or production should be nearly identical (aside from specifying
the environment).


## Staging

Since we do not need to build the cluster from scratch, and since Caktus Tech Support
manages our cluster, we do not need any configuration for AWS Web Stacks or for
ansible-role-k8s-cluster.

These are the steps that we took to provision the staging environment on the Caktus
Saguaro cluster. They DO NOT need to be run again, unless we are re-provisioning it. If
you are looking for documentation on how to deploy updates to the project, look at
[deploy.md](deploy.md). The secrets that are mentioned below are all encrypted in the
repo, but a copy has also been placed in the LastPass entry, "HIP Staging Secrets".


### Set up AWS CLI to use the Caktus Saguaro Cluster account

1. Verify that there is an entry in `~/.aws/credentials` for your main Caktus IAM
   account, typically named `caktus`.

2. Verify that there is an entry in `~/.aws/credentials` for your Caktus Saguaro role.
   Your file should have both of the following entries:

	```conf
	[caktus]
	aws_access_key_id = <your caktus account access key id>
	aws_secret_access_key = <your caktus account secret access key>

	# ...

	[saguaro-cluster]
	role_arn = arn:aws:iam::472354598015:role/CaktusAccountAccessRole-Admins
	source_profile = caktus
	```

	This will allow you to use the special AWS Role that gives accounts in `caktus` full
	privileges in `saguaro-cluster`.

3. Set `AWS_PROFILE` to this named profile. This should be added to your environment
   (using whatever method you use for that: `.envrc`, `.env`, `magical-shell-script.sh`)
   when you switch to this project.

   ```sh
   (hip)$ export AWS_PROFILE=saguaro-cluster
   ```

### Create a docker registry

1. Making sure that your AWS_PROFILE is set, run the command to create a new registry:

   ```sh
   (hip)$ echo $AWS_PROFILE
   saguaro-cluster
   (hip)$ aws ecr create-repository --repository-name hip
   ...
        "repositoryUri": "472354598015.dkr.ecr.us-east-1.amazonaws.com/hip",
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
    (hip)$ aws ecr list-images --repository-name hip
    ... successful output listing an image ...
    ```

### Get access to the cluster

1. Update `tasks.py` and set `cluster` to `caktus-saguaro-cluster` in the
   `ns.configure()` command at the bottom of the file.

2. Get access to the cluster so you can run `kubectl` locally:

    ```sh
    (hip)$ inv aws.configure-eks-kubeconfig
    Updated context arn:aws:eks:us-east-1:472354598015:cluster/caktus-saguaro-cluster
    ...
    ```

### Create a DB on the Saguaro RDS instance

1. Get the RDS params you'll need:

    ```sh
    (hip)$ aws rds describe-db-instances
	```

   * From that output, get `MasterUsername`, `DBName`, and `Endpoint.Address`.
   * Get the `MasterPassword` from the LastPass entry, "Saguaro Cluster Secrets".
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

### Point your desired domain at the load balancer

1. Find the load balancer URL:

	```sh
	(hip)$ kubectl get svc -n ingress-nginx
	```

2. Copy the `EXTERNAL-IP` value from that output. It is the load balancer URL.

3. Go to Cloudflare and create a CNAME from your desired subdomain pointing to that URL.

	```
	hip.caktus-built.com ->	a4c59174c7fff4935b9ab58abd1722e9-742984194.us-east-1.elb.amazonaws.com
	```

### Set up vault password

1. Generate a long password and save it to AWS with this command:

	```sh
	(hip)$ aws secretsmanager create-secret --name hip-ansible-vault-password --secret-string <long-secret>
	{
		"ARN": "arn:aws:secretsmanager:us-east-1:472354598015:secret:hip-ansible-vault-password-KxkJpW",
		"Name": "hip-ansible-vault-password",
		"VersionId": "35d97d2b-7130-407e-bd5c-e59f9d077234"
	}
	```

2. Record the ARN that is returned, you'll need that for setting up CI later

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
   inv staging deploy --tag foo
   ```

4. Take the value from the error output of the previous command, encrypt it, and put the
   encrypted value in `deploy/host_vars/staging.yml` for `k8s_auth_api_key`.

     ```sh
	 cd deploy
	 ansible-vault encrypt_string <secret>
	 ```

5. Repeat step 4 for the other secrets that we need in `host_vars/staging.yaml`
    * `HipDbPassword` from above as `database_password`.
	* Encrypt a long secret key and save it as
      `k8s_environment_variables/DJANGO_SECRET_KEY`.

### Set up email with Amazon SES

Follow these instructions to create a new SMTP user:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html

* IAM User Name: `ses-smtp-user.philly-hip`
* Copy the SMTP Username and SMTP Password and encrypt them to EMAIL_HOST_USER and
  EMAIL_HOST_PASSWORD respectively under the `k8s_environment_variables` heading in
  `deploy/host_vars/staging.yml`.

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

## Production

To be filled out once we provision production.
