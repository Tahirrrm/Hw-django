from django.urls import path
from . import views


urlpatterns = [
    # Публичное
    path('login/', views.portal_login, name='portal_login'),
    path('register/', views.portal_register, name='portal_register'),
    path('logout/', views.portal_logout, name='portal_logout'),
    path('ban/', views.ban_status, name='ban_status'),
    path('articles/', views.articles_public, name='articles_public'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('my-saved/', views.my_saved, name='my_saved'),

    # Админ-панель
    path('admin-panel/', views.dashboard, name='admin_dashboard'),
    path('admin-panel/articles/', views.articles, name='admin_articles'),
    path('admin-panel/articles/new/', views.article_new, name='admin_article_new'),
    path('admin-panel/articles/<int:article_id>/edit/', views.article_edit, name='admin_article_edit'),
    path('admin-panel/articles/<int:article_id>/delete/', views.article_delete, name='admin_article_delete'),
    path('admin-panel/articles/<int:article_id>/toggle/', views.article_toggle_publish, name='admin_article_toggle'),
    path('admin-panel/users/', views.users, name='admin_users'),
    path('admin-panel/users/new/', views.user_add, name='admin_user_add'),
    path('admin-panel/users/<int:user_id>/delete/', views.user_delete, name='admin_user_delete'),
    path('admin-panel/users/<int:user_id>/ban/', views.user_ban, name='admin_user_ban'),
    path('admin-panel/users/<int:user_id>/unban/', views.user_unban, name='admin_user_unban'),
    path('admin-panel/comments/', views.comments, name='admin_comments'),
    path('admin-panel/comments/<int:comment_id>/delete/', views.comment_delete, name='admin_comment_delete'),
    path('admin-panel/settings/', views.settings_view, name='admin_settings'),
    path('admin-panel/stats/', views.stats, name='admin_stats'),
]