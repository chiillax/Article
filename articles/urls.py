from django.urls import path
from .views import ArticleListView, ArticleUpdateView, ArticleDetailView, ArticleDeleteView, ArticleCreateView, UserArticleListView
# from django.conf.urls import url 

urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<author>/', UserArticleListView.as_view(), name="user_articles"),
    # url(r'^([\w-]+)/$', UserArticleListView.as_view(), name="user_articles"),
    path('', ArticleListView.as_view(), name='article_list'),
]
