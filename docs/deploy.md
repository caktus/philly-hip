
# Deploying hip

hip is configured with continuous deployment, but in the eventuality manual deployment is required the following steps will deploy to a configured environment.

## Build and Deploy

The most common uses cases are building images and deploying images, so
this document covers these topics first.

**If this is your first time, please see the [Local Deployment Environment Setup](#local-deployment-environment-setup)
section before continuing.**


### Build

First, make sure your have access to the ECR registry with ``docker``:

```sh
    inv aws.docker-login
```

You should see *Login Succeeded*. If not, make sure you have exported the `hip` [AWS_PROFILE](#1-configure-aws-named-profile).

By default, the next command will perform the following:
* Builds the production Docker image

* Tags the image with the ``{{ branch_name }}-{{ short_commit_sha }}``

* Pushes the image to ECR so it's accessible to EKS for deployment

```sh
$ inv image
```

You should now see the built and tagged image in ``docker images``.


#### Test the Docker image locally

You can test the deployable image locally with:

```sh
$ inv image.up
```

You should see all the supporting containers come up. Then navigate to
http://localhost:8000 you should see the site in it's current state.


### Deploy

If you've just built the image above, the easiest way to deploy it is by running ``docker images`` and
finding the latest image tagged with develop it should look something like this:

```sh
$ 1234567890.dkr.ecr.us-east-1.amazonaws.com/caktu-appli-7ockisoxzjzu   develop-bf47d7b                    ddd65535d290        9 minutes ago       539MB
```

So in the case of the above line you would then run the following to complete a deploy to `staging`:

```sh
$ inv staging deploy --tag=develop-bf47d7b
```


## Local Deployment Environment Setup


### Access to Cluster


#### 1. Configure AWS named profile

Learning power uses the CaktusAccessRole to manage the aws resources for hip.  
If you are unsure of what this means, contact Tech Support.  You should be able to find the credentials for that role in lastpass.

Once you have that setup, you should verify in your `~/.aws/credentials` file there is an entry for the main caktus IAM.

Link your hip profile to the Caktus Main credentials.
  
  1. Edit `~/.aws/credentials`
  1. Either add or make sure you have the following filled out with the right credentials:


```conf
  [<CAKTUS_MAIN_PROFILE_NAME>]
  aws_access_key_id = <LOOK-IN-LASTPASS>
  aws_secret_access_key = <LOOK-IN-LASTPASS>

  ...

  [hip]
  role_arn = arn:aws:iam::<10_DIGIT_hip_ACCOUNT_ID>:role/CaktusAccountAccessRole-Admins
  source_profile = <CAKTUS_MAIN_PROFILE_NAME>
```

1. Edit `~/.aws/profile`
1. Either add or make sure you have the following filled out.

```
[profile hip]
region = <REGION_THIS_PROJECT_IS_IN>
```

Now set the ``AWS_PROFILE`` environment variable to use this named profile:

```sh
$ export AWS_PROFILE=hip
```

Note: If you use ``virtualenvwrapper`` on a Linux machine you can set
``AWS_PROFILE`` in ``postactivate``.


#### 3. Configure cluster context using EKS token

To configure cluster access for the ``kubectl`` command-line tool, with the
``AWS_PROFILE`` defined above, add the cluster context using:

```sh
$ inv aws.configure-eks-kubeconfig
```

You should now have access via ``kubectl``:

```sh
$ kubectl get node
```

## Useful Commands

To see configured ansible variable like ``k8s_environment_variables`` you can use the following invoke command.

```sh
$ inv staging print-ansible-vars
```

To inspect a single variable issue:

```sh
$ inv staging project.print-ansible-vars --var="DATABASE_URL"
```