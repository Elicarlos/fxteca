from django.urls import path
from . views import HomePageView, PostDetailView, AboutPageView, ContactPageView, CategoryPostListView, SearchResultsView, ads_txt


from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, PostSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,  # Opcional, se você tiver um modelo dinâmico
}

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('sobre/', AboutPageView.as_view(), name='about'),
    path('contato/', ContactPageView.as_view(), name='contact'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_posts'),
    path('post_detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('ads.txt', ads_txt, name='ads_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]