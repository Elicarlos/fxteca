from django.urls import path
from . views import HomePageView, PostDetailView, AboutPageView, ContactPageView, CategoryPostListView, SearchResultsView, ads_txt




urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('sobre/', AboutPageView.as_view(), name='about'),
    path('login/', AboutPageView.as_view(), name='login'),
    path('contato/', ContactPageView.as_view(), name='contact'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_posts'),
    path('post_detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('ads.txt', ads_txt, name='ads_txt'),
    
]