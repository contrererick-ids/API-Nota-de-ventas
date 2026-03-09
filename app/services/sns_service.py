import boto3
from app.config import settings

sns_client = boto3.client("sns", region_name=settings.AWS_REGION)

def enviar_notificacion(asunto: str, mensaje: str) -> None:
    sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Subject=asunto,
        Message=mensaje
    )
