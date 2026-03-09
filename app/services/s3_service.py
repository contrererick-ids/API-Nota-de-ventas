import boto3
from datetime import datetime
from app.config import settings

s3_client = boto3.client("s3", region_name=settings.AWS_REGION)

def subir_pdf(pdf_bytes: bytes, rfc: str, folio: str) -> str:
    key = f"{rfc}/{folio}.pdf"
    timestamp = datetime.utcnow().isoformat()

    s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=pdf_bytes,
        ContentType="application/pdf",
        Metadata={
            "hora-envio": timestamp,
            "nota-descargada": "false",
            "veces-enviado": "1"
        }
    )
    return key

def actualizar_metadatos_envio(rfc: str, folio: str) -> None:
    key = f"{rfc}/{folio}.pdf"

    obj = s3_client.head_object(Bucket=settings.S3_BUCKET, Key=key)
    metadata = obj["Metadata"]

    veces = int(metadata.get("veces-enviado", "1")) + 1
    timestamp = datetime.utcnow().isoformat()

    s3_client.copy_object(
        Bucket=settings.S3_BUCKET,
        CopySource={"Bucket": settings.S3_BUCKET, "Key": key},
        Key=key,
        Metadata={
            "hora-envio": timestamp,
            "nota-descargada": metadata.get("nota-descargada", "false"),
            "veces-enviado": str(veces)
        },
        MetadataDirective="REPLACE",
        ContentType="application/pdf"
    )

def marcar_nota_descargada(rfc: str, folio: str) -> None:
    key = f"{rfc}/{folio}.pdf"

    obj = s3_client.head_object(Bucket=settings.S3_BUCKET, Key=key)
    metadata = obj["Metadata"]

    s3_client.copy_object(
        Bucket=settings.S3_BUCKET,
        CopySource={"Bucket": settings.S3_BUCKET, "Key": key},
        Key=key,
        Metadata={
            "hora-envio": metadata.get("hora-envio", ""),
            "nota-descargada": "true",
            "veces-enviado": metadata.get("veces-enviado", "1")
        },
        MetadataDirective="REPLACE",
        ContentType="application/pdf"
    )

def descargar_pdf(rfc: str, folio: str) -> bytes:
    key = f"{rfc}/{folio}.pdf"
    response = s3_client.get_object(Bucket=settings.S3_BUCKET, Key=key)
    return response["Body"].read()