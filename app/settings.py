import os
from pathlib import Path
from decouple import config
import dj_database_url

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta (em produção, esta chave deve estar segura)
SECRET_KEY = config('SECRET_KEY')

# Definindo o modo de debug
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = [
    'fuxicoteca-d2bb0ce5d25a.herokuapp.com',
    '.fuxicoteca-d2bb0ce5d25a.herokuapp.com',
    '127.0.0.1',
    'localhost',
    'fuxicoteca.com.br',
    'www.fuxicoteca.com.br',
]

# Configuração de segurança para SSL


if not DEBUG:
    SECURE_SSL_REDIRECT = False
    
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True  # Se tiver problemas de redirecionamento local, comente em dev

    
# Instalação de apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'storages',      # App para integração com S3
    'ckeditor',
    'ckeditor_uploader',
    'robots',
    'django.contrib.sites',
    'meta',
    'taggit',

    'blog',
]

# ID do site
SITE_ID = 1

# Middlewares
MIDDLEWARE = [
    # Se você usar WhiteNoise, deixe a linha abaixo;
    # Caso não queria usar WhiteNoise, comente-a
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração das URLs
ROOT_URLCONF = 'app.urls'

# Configuração dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Se você usar templates fora do padrão, ajusta aqui
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Seu context processor de categorias:
                'blog.context_processors.categories', 
            ],
        },
    },
]

# Configuração WSGI
WSGI_APPLICATION = 'app.wsgi.application'

# Configuração de banco de dados (Heroku ou ambiente local)
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# sasasasas
# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================================
#  ARMAZENAMENTO NO S3: CONFIGURAÇÕES BÁSICAS
# =========================================================

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# (Exemplo: 'meu-bucket' sem https, sem s3.amazonaws.com no nome, só o bucket mesmo)

# Domínio customizado do S3 (sem espaços)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Local onde os estáticos vão ficar dentro do bucket

# Configurações do S3
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # Cache de 1 dia
}

# Ativar S3 para servir arquivos estáticos
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL base para servir arquivos estáticos
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Se quiser/precisar servir media files via outro backend S3:
# Ex.: app/storage_backends.py (custom class)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# =========================================================
#  CONFIGURAÇÕES LOCAIS DE ARQUIVOS ESTÁTICOS (collectstatic)
# =========================================================

# Diretórios (local) de onde coletar estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # pasta local com assets do seu projeto
]

# Para onde o Django move os arquivos estáticos localmente (quando não se usa S3)
# Necessário mesmo usando S3, pois o Django gera uma pasta temporária
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =========================================================
#  CKEDITOR
# =========================================================
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        'extraPlugins': 'codesnippet',
        "toolbar": "full",
        "height": 400,
        "width": "auto",
        'codeSnippet_theme': 'monokai_sublime',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['CodeSnippet'],
            ['Link', 'Unlink'],
            ['Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'Image', 'Table', 'HorizontalRule'],
        ],
        "extraPlugins": "image2",
        "filebrowserUploadUrl": "/ckeditor/upload/",
        "filebrowserBrowseUrl": "/ckeditor/browse/",
    },
}

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


# =========================================================
#  LOGGING
# =========================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
