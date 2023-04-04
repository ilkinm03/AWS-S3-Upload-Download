import dotenv
import boto3
from botocore.client import Config

config = dotenv.dotenv_values(".env")

choice = input("Download / Upload? ").strip().lower()

file_name = input("Enter the file name: ").strip()

if choice == "upload":
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=config.get("ACCESS_KEY_ID"),
        aws_secret_access_key=config.get("ACCESS_SECRET_KEY"),
        config=Config(signature_version="s3v4")
    )

    target_file_path = input(
        "Enter the target file relative path with the filename and extension:\n"
    ).strip()
    file_mime = input("Enter the file mime type: ").strip().lower()

    with open(target_file_path, "rb") as f:
        s3.Bucket(config.get("BUCKET_NAME")).put_object(
            Key=file_name,
            Body=f,
            ContentType=file_mime,
        )
elif choice == "download":
    download_path = input(
        "Enter the path with filename and extension where you want to download:\n"
    ).strip()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=config.get("ACCESS_KEY_ID"),
        aws_secret_access_key=config.get("ACCESS_SECRET_KEY"),
    )

    s3.download_file(
        Bucket=config.get("BUCKET_NAME"),
        Key=file_name,
        Filename=download_path,
    )

print("Done")
