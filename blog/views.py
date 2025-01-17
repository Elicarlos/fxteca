from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from blog.forms import CommentForm
from . models import Category, Post, Comment
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.paginator import Paginator
import os
from django.db.models import Q


def test_template(request):
    template = get_template('base.html')  # Teste se o Django encontra o template
    return HttpResponse(template.render())

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10  # para evitar lógica manual de paginator

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Filtra por is_published e busca no título/conteúdo
            return Post.objects.filter(is_published=True).filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).order_by('-created_at')
        return Post.objects.none()



def loaderio(request):
    file_path = os.path.join('static', 'loaderio-9a3569bfec7a5734fa323fb30ca12d97.txt')  # Ajuste o caminho se necessário
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename=ads.txt'
        return response
    
def ads_txt(request):
    file_path = os.path.join('static', 'ads.txt')  # Ajuste o caminho se necessário
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename=ads.txt'
        return response

class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-created_at')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Inclui 'destaque' (primeiro post com destaque ou então o mais recente)
        e substitui 'posts' para pegar os próximos 3 (exemplo).
        Mas cuidado: isto pode interferir na paginação.
        """
        context = super().get_context_data(**kwargs)

        # Pega o post com destaque (se existir), senão o mais recente
        destaque = Post.objects.filter(is_published=True, destaque=True).first()
        if not destaque:
            destaque = Post.objects.filter(is_published=True).order_by('-created_at').first()
        context['destaque'] = destaque

        # Pega mais 3 posts, pulando o primeiro
        # Se 'destaque' for o mesmo que queryset[0], isso funciona, mas pode gerar confusão com paginated posts
        context['recent_posts'] = Post.objects.filter(is_published=True).order_by('-created_at')[1:4]

        return context

    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
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
                try:
                    comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    comment.parent = None
            comment.save()
            return redirect('post_detail', slug=self.object.slug)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comentários principais aprovados
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


