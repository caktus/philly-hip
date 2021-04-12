# Deploying HIP

HIP is configured with continuous deployment, but here are the steps to perform a manual
deployment from your laptop.

**If this is your first time, please see the [Local Deployment Environment Setup](#local-deployment-environment-setup) section before continuing.**

## Build

First, make sure your have access to the ECR registry with ``docker``:

```sh
(hip)$ inv aws.docker-login
```

You should see *Login Succeeded*. If not, make sure you have set your
[AWS_PROFILE](#configure-aws-named-profile) correctly.

By default, the next command will perform the following:
* Builds the production Docker image

* Tags the image with the ``{{ branch_name }}-{{ short_commit_sha }}``

* Pushes the image to ECR so it's accessible to EKS for deployment

```sh
(hip)$ inv image
```

You should now see the built and tagged image in ``docker images``.


### Test the Docker image locally

You can test the deployable image locally with:

```sh
(hip)$ inv image.up
```

You should see all the supporting containers come up. When you navigate to
http://localhost:8000, you should see the site in its current state.


## Deploy

If you've just built the image above, the easiest way to deploy it is by running ``docker images`` and
finding the latest image tagged with develop it should look something like this:

```sh
(hip)$ docker images
...
1234567890.dkr.ecr.us-east-1.amazonaws.com/caktu-appli-7ockisoxzjzu   develop-bf47d7b                    ddd65535d290        9 minutes ago       539MB
...
```

So in the case of the above line you would then run the following to complete a deploy to `staging`:

```sh
(hip)$ inv staging deploy --tag=develop-bf47d7b
```


## Build and Deploy in one command

To build and deploy in a single command:

```sh
(hip)$ inv staging image deploy
```

## Update or add a secret to the deployment

If you need to add or change a secret in your environment, you'll first need to encrypt
it and then add the encrypted value to your `deploy/host_vars/<environment>.yml` file,
where `<environment>` represents the name of the environment you are updating, usually
"staging" or "production.

1. Generate or obtain the new secret. Then encrypt it with this command:

    ```sh
    (hip)$ cd deploy
    (hip)$ ansible-vault encrypt_string <secret>
    !vault |
              $ANSIBLE_VAULT;1.1;AES256
              38646465363539613435316335663835373561346262383832303439623533376564636465666535
              3663396663373465633465636639636631303232343732380a343034376633323330386337653930
              36643366636334643839363763366335343266643431346435636264623634616538373863393534
              3937643532306231610a626333656461386433303335373361323330323466666130303063303863
              30623762363233643337653961633062346537643066663837633535336164623663
    Encryption successful
    ```
2. Copy everything from the `!vault` up until the `Encryption successful` message, but
   not including the `Encryption successful` message.

3. Paste it into `deploy/host_vars/<environment>.yml` as the value for the key that you
   are adding or changing.

## Running commands on a deployed enviroment

At a minimum, you may want to create a superuser for yourself on staging. Here is the
command to do that.

```sh
(hip)$ inv staging pod.shell
appuser@app-84f486b849-pfp7k:/code$ python manage.py createsuperuser
Email: me@example.com
Password:
Password (again):
Superuser created successfully.
appuser@app-84f486b849-pfp7k:/code$ exit
```

If you get a `namespaces "hip-staging" not found` error, check out the "Configure access
to the kubernetes cluster" section below to configure your local machine to have access
to the cluster.

## Local Deployment Environment Setup

### Configure AWS named profile

1. Verify that there is an entry in `~/.aws/credentials` for your main Caktus IAM
   account, typically named `caktus` (which is what we'll assume it is for these
   instructions).

2. Verify that there is an entry in `~/.aws/credentials` for the `philly-hip` role.
   Your file should have both of the following entries:

    ```conf
    [caktus]
    aws_access_key_id = <your caktus account access key id>
    aws_secret_access_key = <your caktus account secret access key>

    # ...

    [philly-hip]
    role_arn = arn:aws:iam::061553509755:role/CaktusAccountAccessRole-Admins
    source_profile = caktus
    region = us-east-1
    ```

    This will allow you to use the special AWS Role that we have set up that gives
    accounts in `caktus` full privileges in `philly-hip`.

3. Set `AWS_PROFILE` to this named profile. This should be added to your environment
   (using whatever method you use for that: `.envrc`, `.env`, `magical-shell-script.sh`)
   when you switch to this project.

   ```sh
   (hip)$ export AWS_PROFILE=philly-hip
   ```

### Confirm access to docker registry

1. Make sure you can successfully login to the docker repo. This login does expire from
    time to time, so you may have to re-run the command before a deploy.

    ```sh
    (hip)$ echo $AWS_PROFILE
    philly-hip
    (hip)$ inv aws.docker-login
    ```

### Configure access to the kubernetes cluster

1. Configure your local machine to access the cluster using ``kubectl``.

   ```sh
   (hip)$ echo $AWS_PROFILE
   philly-hip
   (hip)$ inv aws.configure-eks-kubeconfig
   ```

2. You should now have access via ``kubectl``:

    ```sh
    (hip)$ kubectl get node
    ```

### Get access to the AWS Console:

If you need access to the AWS Console, create a bookmark with this URL:

https://signin.aws.amazon.com/switchrole?roleName=CaktusAccountAccessRole-Admins&account=061553509755&displayName=Philly-PDPH

If you are logged into the AWS console with your `caktus` account, then that URL will
switch you to the PDPH subaccount.

Reference: https://github.com/caktus/caktus-hosting-services/blob/main/docs/aws-assumerole.md#aws-accounts

### Useful Commands

To see configured ansible variable like ``k8s_environment_variables`` you can use the following invoke command.

```sh
(hip)$ inv staging info.print-ansible-vars
```

There are many other useful commands built into `invoke-kubesae` itself, so check out
its [documentation](https://github.com/caktus/invoke-kubesae).
