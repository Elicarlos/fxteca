from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post

# Exemplo para URLs estáticas (páginas que não dependem de um banco de dados)
class PostSitemap(Sitemap):
    changefreq = "daily"  # Frequência de atualização do conteúdo
    priority = 0.8        # Prioridade do conteúdo

    def items(self):
        return Post.objects.filter(is_published=True)  # Apenas posts publicados

    def lastmod(self, obj):
        return obj.updated_at  # Última modificação do post

    def location(self, obj):
        return obj.get_absolute_url()
