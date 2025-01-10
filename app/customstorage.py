from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os

# Configuração para garantir que o S3 utilize sigv4 (recomendado para AWS)
os.environ['S3_USE_SIGV4'] = 'True'

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION  # A pasta onde os arquivos estáticos serão armazenados no S3

    # Defina o host do S3, caso seja necessário para um region específico (como na AWS S3)
    # Isso pode ser útil se você tiver uma configuração customizada de bucket.
    host = "s3-%s.amazonaws.com" % settings.AWS_REGION

    # A conexão é criada automaticamente pelo S3Boto3Storage, mas se você precisar
    # de algo customizado, pode manter essa configuração.
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format, host=self.host)
        return self._connection


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION  # A pasta onde os arquivos de mídia serão armazenados no S3
    host = "s3-%s.amazonaws.com" % settings.AWS_REGION  # Definindo o host para a região da AWS

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format, host=self.host)
        return self._connection

