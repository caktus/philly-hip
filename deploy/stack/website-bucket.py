# Website-enabled S3 bucket CloudFormation Template
#
# See docs/website-bucket.md for more information.
#

from troposphere import GetAtt, Join, Output, Parameter, Ref, Template, s3


template = Template()

bucket_name = template.add_parameter(
    Parameter(
        "WebsiteBucketName",
        Description="Name for the website asset bucket",
        Type="String",
    ),
)

website_bucket = template.add_resource(
    s3.Bucket(
        "WebsiteBucket",
        BucketName=Ref(bucket_name),
        AccessControl="PublicRead",
        VersioningConfiguration=s3.VersioningConfiguration(Status="Enabled"),
        DeletionPolicy="Retain",
        WebsiteConfiguration=s3.WebsiteConfiguration(
            IndexDocument="index.html",
        ),
    )
)

website_bucket_policy = template.add_resource(
    s3.BucketPolicy(
        "WebsiteBucketPolicy",
        PolicyDocument=dict(
            Statement=dict(
                Effect="Allow",
                Principal="*",
                Action=["s3:GetObject"],
                Resource=Join("", ["arn:aws:s3:::", Ref(website_bucket), "/*"]),
            ),
        ),
        Bucket=Ref(website_bucket),
    )
)

template.add_output(
    [
        Output(
            "WebsiteBucketURL",
            Value=GetAtt(website_bucket, "WebsiteURL"),
            Description="URL for website hosted on S3",
        ),
        Output(
            "WebsiteBucketSecureURL",
            Value=Join("", ["https://", GetAtt(website_bucket, "DomainName")]),
            Description="Secure URL for website hosted on S3",
        ),
    ]
)

print(template.to_yaml())
