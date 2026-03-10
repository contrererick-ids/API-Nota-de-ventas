from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    EC2_HOST: str
    S3_BUCKET: str
    AWS_REGION: str
    SNS_TOPIC_ARN: str

    class Config:
        env_file = ".env"

# Se genera un objeto de tipo Settings para acceder a las variables de entorno del proyecto
settings = Settings()
