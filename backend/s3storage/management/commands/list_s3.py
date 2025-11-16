from django.core.management.base import BaseCommand
import boto3
from django.conf import settings

class Command(BaseCommand):
    help = 'List all files in S3 bucket'

    def add_arguments(self, parser):
        parser.add_argument(
            '--download',
            type=str,
            help='Download a specific file by key',
        )

    def handle(self, *args, **options):
        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        
        # Download specific file
        if options['download']:
            try:
                file_key = options['download']
                local_path = f'/tmp/{file_key.split("/")[-1]}'
                s3.download_file(bucket, file_key, local_path)
                self.stdout.write(self.style.SUCCESS(f'Downloaded to: {local_path}'))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error downloading: {str(e)}'))
                return
        
        try:
            # List buckets
            buckets = s3.list_buckets()
            self.stdout.write(self.style.SUCCESS('\n=== Available Buckets ==='))
            for b in buckets['Buckets']:
                self.stdout.write(f"  📦 {b['Name']}")
            
            # List objects
            response = s3.list_objects_v2(Bucket=bucket)
            
            if 'Contents' in response:
                self.stdout.write(self.style.SUCCESS(f'\n=== Files in {bucket} ==='))
                total_size = 0
                for obj in response['Contents']:
                    size_kb = obj['Size'] / 1024
                    total_size += obj['Size']
                    date = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
                    self.stdout.write(f"  📄 {obj['Key']}")
                    self.stdout.write(f"     Size: {size_kb:.2f} KB | Modified: {date}")
                
                self.stdout.write(self.style.SUCCESS(f'\nTotal: {len(response["Contents"])} files, {total_size/1024:.2f} KB'))
            else:
                self.stdout.write(self.style.WARNING(f'\n{bucket} is empty'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            