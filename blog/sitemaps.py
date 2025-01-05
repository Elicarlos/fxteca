from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post

# Exemplo para URLs estáticas (páginas que não dependem de um banco de dados)
class StaticViewSitemap(Sitemap):
    priority = 0.8  # Relevância (1.0 = mais alta, 0.0 = mais baixa)
    changefreq = 'weekly'  # Frequência de atualização (ex.: 'daily', 'monthly')

    def items(self):
        # Retorna os nomes das views estáticas que devem aparecer no sitemap
        return ['index', 'about', 'contact']

    def location(self, item):
        # Gera o link para cada view usando o `reverse()`
        return reverse(item)
    
class PostSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Post.objects.filter(is_published=True)  # Filtra itens publicados

    def lastmod(self, obj):
        return obj.updated_at
