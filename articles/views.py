from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    login_url = 'login'
    ordering = ['-date']

    # def get_queryset(self):
    #     return Article.objects.filter(author=self.request.user)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article/article_new.html'
    fields = ('title', 'body',)
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/article_detail.html'
    login_url = 'login'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article/article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class UserArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    login_url = 'login'
    ordering = ['-date']

    def get_queryset(self):
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['author'])
        return Article.objects.filter(author=self.author)
        # self.username = get_object_or_404(get_user_model(), username=self.args[0])
        # return Article.objects.filter(author=self.username)
