from django.contrib import admin
from .models import Article, Comment, SavedArticle, UserBan, SiteSettings


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views_count', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    search_fields = ('text',)


@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')


@admin.register(UserBan)
class UserBanAdmin(admin.ModelAdmin):
    list_display = ('user', 'banned_until', 'created_at')
    search_fields = ('user__username',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('background_color', 'font_color', 'font_size')