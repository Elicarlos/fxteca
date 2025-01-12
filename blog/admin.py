from django.contrib import admin
from .models import Post, Category, Comment
from taggit.models import Tag
from .forms import CommentForm  # Assegure-se de ter um formulário de comentário

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentForm
    list_display = ('post', 'author', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'structured_data': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80,
                'placeholder': 'Insira dados estruturados em JSON-LD aqui...'
            }),
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'slug', 'created_at', 'author', 'category', 'is_published', 'destaque')
    prepopulated_fields = {'slug': ('title',)}  # Gera automaticamente no admin
    readonly_fields = ('created_at', 'updated_at') 
    list_filter = ('category', 'is_published', 'destaque') 
    search_fields = ('title', 'content', 'author__username', 'tags__name')
    
    # Organizando os campos em fieldsets
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'highlight_summary', 'list_summary', 'image', 'detail_image')
        }),
        ('Informações Gerais', {
            'fields': ('author', 'category', 'tags', 'is_published', 'destaque')
        }),
        ('SEO Básico', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'meta_author', 'canonical_url')
        }),
        ('Open Graph', {
            'classes': ('collapse',),
            'fields': ('og_title', 'og_description', 'og_image')
        }),
        ('Twitter Cards', {
            'classes': ('collapse',),
            'fields': ('twitter_title', 'twitter_description', 'twitter_image')
        }),
        ('Dados Estruturados', {
            'classes': ('collapse',),
            'fields': ('structured_data',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Opcional: Adicionar hierarquia de datas para facilitar a navegação
    date_hierarchy = 'created_at'
