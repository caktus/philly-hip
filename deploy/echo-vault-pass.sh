#!/bin/sh
# Prints the Ansible vault password retrieved from the AWS Secrets Manager
# for use by --vault-password-file. See: https://devops.stackexchange.com/a/733
# You can manage secrets here:
# https://us-west-2.console.aws.amazon.com/secretsmanager/home?region=us-west-2#/listSecrets
# This is a "plaintext" secret containing a long random string.
set -e
export SECRET_ID="hip-ansible-vault-password"
aws secretsmanager get-secret-value --secret-id ${SECRET_ID} --query SecretString --output text
