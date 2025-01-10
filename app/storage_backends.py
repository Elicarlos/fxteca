from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

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