from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.html import strip_tags
from django.urls import reverse


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comentário de {self.author} em {self.post.title}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    highlight_summary = models.TextField(null=True, blank=True, verbose_name="Resumo de Destaque")
    list_summary = models.TextField(null=True, blank=True, verbose_name="Resumo da Lista")
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    detail_image = models.ImageField(upload_to='posts/details/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = TaggableManager()
    keywords = models.TextField(null=True, blank=True, help_text="Palavras-chave separadas por vírgulas.")
    canonical_url = models.URLField(null=True, blank=True, help_text="URL canônica para evitar duplicação.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destaque = models.BooleanField(default=False) 
    is_published = models.BooleanField(default=True)
    
    # Campos adicionais para SEO
    meta_title = models.CharField(max_length=60, null=True, blank=True, help_text="Título para SEO, até 60 caracteres.")
    meta_description = models.TextField(null=True, blank=True, help_text="Descrição para SEO, até 160 caracteres.")
    meta_robots = models.CharField(max_length=20, choices=[
        ('index, follow', 'Index, Follow'),
        ('noindex, nofollow', 'No Index, No Follow'),
        ('noindex, follow', 'No Index, Follow'),
        ('index, nofollow', 'Index, No Follow'),
    ], default='index, follow')
    
    # Campos para Open Graph
    og_title = models.CharField(max_length=60, null=True, blank=True, help_text="Título para Open Graph.")
    og_description = models.TextField(null=True, blank=True, help_text="Descrição para Open Graph.")
    og_image = models.ImageField(upload_to='og_images/', null=True, blank=True, help_text="Imagem para Open Graph.")
    
    # Campos para Twitter Cards
    twitter_title = models.CharField(max_length=60, null=True, blank=True, help_text="Título para Twitter Cards.")
    twitter_description = models.TextField(null=True, blank=True, help_text="Descrição para Twitter Cards.")
    twitter_image = models.ImageField(upload_to='twitter_images/', null=True, blank=True, help_text="Imagem para Twitter Cards.")
    
    # Dados Estruturados
    structured_data = models.JSONField(null=True, blank=True, help_text="Dados estruturados em JSON-LD.")
    
    def generate_summary(self, content, caracteres):
        """Gera um resumo baseado no conteúdo e no número de caracteres."""
        if not content:
            return "Sem resumo disponível."
        clean_content = strip_tags(content)
        if len(clean_content) > caracteres:
            return clean_content[:caracteres].rsplit(' ', 1)[0] + "..."
        return clean_content

    def get_highlight_summary(self):
        """Retorna o resumo do destaque ou gera automaticamente."""
        return self.highlight_summary or self.generate_summary(self.content, 200)

    def get_list_summary(self):
        """Retorna o resumo da lista ou gera automaticamente."""
        return self.list_summary or self.generate_summary(self.content, 100)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_meta_description(self):
        return self.meta_description or self.content[:150]

    def get_meta_keywords(self):
        if self.keywords:
            return self.keywords
        return ', '.join(tag.name for tag in self.tags.all())

    def get_meta_author(self):
        return self.author.get_full_name() if self.author else "Fuxicoteca"

    def get_meta_image(self):
        return self.image.url if self.image else None

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    @property
    def meta_description_content(self):
        return self.get_meta_description()

    @property
    def meta_keywords_content(self):
        return self.get_meta_keywords()

    @property
    def meta_author_content(self):
        return self.get_meta_author()

    @property
    def meta_image_content(self):
        return self.get_meta_image()
