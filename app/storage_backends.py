from storages.backends.s3boto3 import S3Boto3Storage

# Armazenamento para arquivos de mídia
class MediaStorage(S3Boto3Storage):
    location = 'media'  # Pasta dentro do bucket S3 para armazenar mídias
    file_overwrite = False  # Não sobrescrever arquivos com o mesmo nome

# Armazenamento para arquivos estáticos
class StaticStorage(S3Boto3Storage):
    location = 'static'  # Pasta dentro do bucket S3 para armazenar arquivos estáticos
    file_overwrite = False  # Não sobrescrever arquivos estáticos com o mesmo nome
