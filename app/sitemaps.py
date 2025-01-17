from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = "daily"  # Frequência de atualização (exemplo: daily, weekly)
    priority = 0.8  # Prioridade entre 0.0 e 1.0

    def items(self):
        # Retorna os posts publicados
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        # Retorna a data da última modificação do post
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        # Define as URLs estáticas a serem incluídas no sitemap
        return ['about', 'contact']

    def location(self, item):
        return reverse(item)
