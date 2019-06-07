from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'date']
    inlines = [CommentInline, ]

    class Meta:
        model = Article

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'date', 'article']

    class Meta:
        model = Comment


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
