from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormMixin
from django.urls import reverse_lazy
from .models import Article
from .form import CommentForm
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


class ArticleDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Article
    template_name = 'article/article_detail.html'
    login_url = 'login'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super(ArticleDetailView, self).form_valid(form)

    def form_invalid(self, form):
        # put logi
        return super(ArticleDetailView, self).form_invalid(form)


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
        self.author = get_object_or_404(
            get_user_model(), username=self.kwargs['author'])
        return Article.objects.filter(author=self.author)
        # self.username = get_object_or_404(get_user_model(), username=self.args[0])
        # return Article.objects.filter(author=self.username)
