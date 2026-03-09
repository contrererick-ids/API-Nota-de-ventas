import boto3
from app.config import settings

s3_client = boto3.client("s3", region_name=settings.AWS_REGION)

def subir_archivo(archivo_bytes: bytes, nombre_archivo: str, content_type: str) -> str:
    s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=nombre_archivo,
        Body=archivo_bytes,
        ContentType=content_type
    )
    url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{nombre_archivo}"
    return url

def eliminar_archivo(nombre_archivo: str) -> None:
    s3_client.delete_object(
        Bucket=settings.S3_BUCKET,
        Key=nombre_archivo
    )

def obtener_url_presignada(nombre_archivo: str, expiracion: int = 3600) -> str:
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": nombre_archivo},
        ExpiresIn=expiracion
    )
    return url
