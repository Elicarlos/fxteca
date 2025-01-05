from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.html import strip_tags


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
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    highlight_summary = models.TextField(null=True, blank=True, verbose_name="Resumo de Destaque")
    list_summary = models.TextField(null=True, blank=True, verbose_name="Resumo da Lista")
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    detail_image = models.ImageField(upload_to='posts/details/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destaque = models.BooleanField(default=False) 
    is_published = models.BooleanField(default=True)
    
    
    def generate_summary(self, content, caracteres):
        """Gera um resumo baseado no conteúdo e no número de caracteres."""
        from django.utils.html import strip_tags
        if not content:
            return "Sem resumo disponível."
        clean_content = strip_tags(content)
        return clean_content[:caracteres] + "..." if len(clean_content) > caracteres else clean_content

    def get_highlight_summary(self):
        """Retorna o resumo do destaque ou gera automaticamente."""
        return self.highlight_summary or self.generate_summary(self.content, 200)

    def get_list_summary(self):
        """Retorna o resumo da lista ou gera automaticamente."""
        return self.list_summary or self.generate_summary(self.content, 100)

    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    _metadata = {
        'title': 'title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'author': 'get_meta_author',
        'image': 'get_meta_image',
        'url': 'get_absolute_url',
    }
  
    def get_meta_description(self):
        return self.content[:150]

    def get_meta_keywords(self):
        return ', '.join(tag.name for tag in self.tags.all())

    def get_meta_author(self):
        return self.author.get_full_name() if self.author else "Fuxicoteca"

    def get_meta_image(self):
        return self.image.url if self.image else None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})
    
