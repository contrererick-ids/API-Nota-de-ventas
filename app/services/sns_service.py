import boto3
from app.config import settings

sns_client = boto3.client("sns",
                          region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          aws_session_token=settings.AWS_SESSION_TOKEN
                         )

def enviar_notificacion(asunto: str, mensaje: str) -> None:
    sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Subject=asunto,
        Message=mensaje
    )
