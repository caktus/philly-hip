import boto3


session = boto3.Session(profile_name="saguaro-cluster")
credentials = session.get_credentials().get_frozen_credentials()

print(f'export AWS_ACCESS_KEY_ID="{credentials.access_key}"')
print(f'export AWS_SECRET_ACCESS_KEY="{credentials.secret_key}"')
print(f'export AWS_SECURITY_TOKEN="{credentials.token}"')
print(f'export AWS_SESSION_TOKEN="{credentials.token}"')
