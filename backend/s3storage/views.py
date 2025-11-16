import boto3
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


class FileAPIView(APIView):
    """DRF APIView for uploading and listing files in S3/LocalStack"""

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error":"No file provided"}, status=HTTP_400_BAD_REQUEST)
        
        filename = default_storage.save(f'uploads/{uploaded_file.name}', uploaded_file)
        file_url = default_storage.url(filename)

        public_url = file_url.replace("localstack", "localhost")
        
        return_data = {
            "success": True,
            "filename": filename,
            "url": public_url
        }

        return Response(return_data, status=HTTP_201_CREATED)
    
    def get(self, request):
        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )

        try:
            response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            files = []

            if "Contents" in response:
                for obj in response["Contents"]:
                    files.append({
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat()
                    })
            
            return_data = {"files": files}
            return Response(return_data, status=HTTP_200_OK)
        except Exception as e:
            return_data = {"error": str(e)}
            return Response(return_data, status=HTTP_500_INTERNAL_SERVER_ERROR)
        