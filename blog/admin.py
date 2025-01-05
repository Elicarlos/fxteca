from django.contrib import admin
from . models import Post, Category
from taggit.models import Tag 

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'author', 'category')
    prepopulated_fields = {'slug': ('title',)}  # Gera automaticamente no admin
    fields = ('title', 'slug', 'content',  'highlight_summary', 'list_summary', 'image', 'detail_image', 'author', 'category', 'tags', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at') 
    list_filter = ('category',) 
    