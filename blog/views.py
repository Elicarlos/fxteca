from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from blog.forms import CommentForm
from . models import Category, Post, Comment
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.paginator import Paginator
import os


def test_template(request):
    template = get_template('base.html')  # Teste se o Django encontra o template
    return HttpResponse(template.render())

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query) if query else Post.objects.none()
            paginator = Paginator(queryset, 10)  # 10 posts por página
            page_number = self.request.GET.get('page')
            return paginator.get_page(page_number)
        return Post.objects.none()

def post_detail(request):
    return HttpResponse('detail')

def ads_txt(request):
    file_path = os.path.join('static', 'ads.txt')  # Ajuste o caminho se necessário
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename=ads.txt'
        return response

class HomePageView(ListView):
    model = Post
    template_name =  'blog/home.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-created_at')
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Selecionar o destaque ou o último post
        destaque = Post.objects.filter(is_published=True, destaque=True).first()
        if not destaque:
            destaque = Post.objects.filter(is_published=True).order_by('-created_at').first()
        context['destaque'] = destaque
        context['posts'] = Post.objects.filter(is_published=True).order_by('-created_at')[1:4]
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name =  'blog/post_detail.html'
    context_object_name = 'post'  
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect('post_detail', slug=self.object.slug)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comentários principais
        root_comments = self.object.comments.filter(parent__isnull=True, is_approved=True)
        context['root_comments'] = root_comments
        
        # Respostas aprovadas para cada comentário
        context['approved_replies'] = {comment.id: comment.replies.filter(is_approved=True) for comment in root_comments}
        
        # Formulário de comentário
        context['comment_form'] = CommentForm()
        return context
    
class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])  # Adiciona a categoria ao contexto
        return context

    
class AboutPageView(DetailView):
    model = Post
    template_name =  'blog/about.html'
    context_object_name = 'posts'
 
    
class ContactPageView(DetailView):
    model = Post
    template_name =  'blog/home.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-created_at')
    paginate_by = 5


