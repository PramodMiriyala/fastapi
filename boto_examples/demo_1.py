"""This is aws python sdk sample """
import boto3

# s3 = boto3.resource('s3')
# bucket_list = s3.buckets.all()
# print([x.name for x in bucket_list])

# client = boto3.client("s3")
# buckets = client.list_buckets(
#     )
# if __name__ == "__main__":
#     print(buckets["Buckets"][0]["Name"])

client = boto3.client('ec2')
valid_regions = client.describe_regions()
region_list = (valid_regions["Regions"])
print([x["RegionName"] for x in region_list])