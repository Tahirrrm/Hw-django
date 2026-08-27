from datetime import timedelta

from django.contrib.auth import login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Article, Comment, SavedArticle, UserBan, SiteSettings


ADMIN_GROUP_NAME = 'Администраторы'
BAN_DURATIONS = {
    'day': ('День', timedelta(days=1)),
    'week': ('Неделя', timedelta(weeks=1)),
    'month': ('Месяц', timedelta(days=30)),
    'forever': ('Навсегда', None),
}


# --------------------------------------------------------------------------
# Вспомогательные функции
#
# 1) Группа/роль администрирования портала.
#    Права администратора проверяются через membership в группе
#    «Администраторы», а НЕ по флагу is_staff/is_superuser.
#    Группу и нескольких её участников создаёт команда
#    `python manage.py setup_admin`.
#
# 2) Декоратор admin_required защищает все представления панели:
#    доступ разрешён только авторизованному участнику группы.
# --------------------------------------------------------------------------

def get_admin_group():
    group, _ = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
    return group


def user_is_admin(user):
    return user.is_authenticated and user.groups.filter(name=ADMIN_GROUP_NAME).exists()


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not user_is_admin(request.user):
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path(), login_url='portal_login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def _error_page(request, message):
    return render(request, 'portal/error.html', {'message': message})


# --------------------------------------------------------------------------
# Публичные страницы: вход, регистрация, бан
# --------------------------------------------------------------------------

def portal_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ban = getattr(user, 'ban', None)
            if ban is not None and ban.is_active():
                return redirect('ban_status')
            next_url = request.GET.get('next') or 'articles_public'
            return redirect(next_url)
        return render(request, 'portal/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'portal/login.html')


def portal_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        errors = []
        if not username or not password:
            errors.append('Логин и пароль обязательны.')
        elif User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким логином уже существует.')
        else:
            try:
                validate_password(password)
            except ValidationError as exc:
                errors.extend(list(exc.messages))
        if errors:
            return render(request, 'portal/register.html', {
                'errors': errors, 'username': username, 'email': email,
            })
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('articles_public')
    return render(request, 'portal/register.html')


def portal_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('portal_login')
    return redirect('portal_login')


@login_required(login_url='portal_login')
def ban_status(request):
    ban = getattr(request.user, 'ban', None)
    forever = ban is not None and ban.is_forever
    return render(request, 'portal/ban_status.html', {
        'ban': ban, 'forever': forever,
    })


# --------------------------------------------------------------------------
# Админ-панель: главная
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def dashboard(request):
    settings = SiteSettings.get_solo()
    context = {
        'articles_count': Article.objects.count(),
        'published_count': Article.objects.filter(is_published=True).count(),
        'comments_count': Comment.objects.count(),
        'users_count': User.objects.count(),
        'banned_count': UserBan.objects.filter(
            Q(banned_until__isnull=True) | Q(banned_until__gt=timezone.now())
        ).count(),
        'settings': settings,
        'admin_group': get_admin_group(),
    }
    return render(request, 'portal/dashboard.html', context)


# --------------------------------------------------------------------------
# Админ-панель: статьи (новости)
# Соответствует пункту «Администратор может публиковать новости и статьи,
# удалять материалы, редактировать материалы».
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def articles(request):
    """Список всех материалов (для управления и сортировки)."""
    items = Article.objects.select_related('author').all()
    return render(request, 'portal/article_list.html', {'items': items, 'settings': None})


@login_required(login_url='portal_login')
@admin_required
def article_new(request):
    """Публикация новой статьи/новости (POST → создание записи)."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        short = request.POST.get('short_text', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        if not title or not content:
            return render(request, 'portal/article_form.html', {
                'form_error': 'Заголовок и содержание обязательны.', 'article': None,
            })
        Article.objects.create(
            title=title, short_text=short, content=content,
            author=request.user, is_published=is_published,
        )
        return redirect('admin_articles')
    return render(request, 'portal/article_form.html', {'article': None})


@login_required(login_url='portal_login')
@admin_required
def article_edit(request, article_id):
    """Редактирование материала (заголовок, текст, публикация/черновик)."""
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        short = request.POST.get('short_text', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        if not title or not content:
            return render(request, 'portal/article_form.html', {
                'form_error': 'Заголовок и содержание обязательны.', 'article': article,
            })
        article.title = title
        article.content = content
        article.short_text = short
        article.is_published = is_published
        article.save()
        return redirect('admin_articles')
    return render(request, 'portal/article_form.html', {'article': article})


@login_required(login_url='portal_login')
@admin_required
def article_delete(request, article_id):
    """Удаление материала (с подтверждением на отдельной странице)."""
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('admin_articles')
    return render(request, 'portal/confirm_delete.html', {
        'object_label': f'Статью «{article.title}»', 'url': request.get_full_path(),
    })


@login_required(login_url='portal_login')
@admin_required
def article_toggle_publish(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.is_published = not article.is_published
    article.save()
    return redirect('admin_articles')


# --------------------------------------------------------------------------
# Админ-панель: пользователи
# Соответствует пункту «Администратор может добавлять пользователей,
# удалять пользователей, банить пользователей на какой-то срок:
# День / Неделя / Месяц / Навсегда» (+ разбан из того же раздела).
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def users(request):
    items = User.objects.all().order_by('-date_joined')
    return render(request, 'portal/user_list.html', {'items': items})


@login_required(login_url='portal_login')
@admin_required
def user_add(request):
    """Добавление пользователя администратором; при необходимости
    новый пользователь сразу включается в группу «Администраторы»."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        is_admin = request.POST.get('is_admin') == 'on'
        errors = []
        if not username or not password:
            errors.append('Логин и пароль обязательны.')
        elif User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким логином уже существует.')
        if errors:
            return render(request, 'portal/user_form.html', {'errors': errors})
        user = User.objects.create_user(username=username, password=password, email=email)
        if is_admin:
            get_admin_group().user_set.add(user)
        return redirect('admin_users')
    return render(request, 'portal/user_form.html')


@login_required(login_url='portal_login')
@admin_required
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        if user == request.user:
            return _error_page(request, 'Нельзя удалить самого себя.')
        user.delete()
        return redirect('admin_users')
    return render(request, 'portal/confirm_delete.html', {
        'object_label': f'Пользователя {user.username}', 'url': request.get_full_path(),
    })


@login_required(login_url='portal_login')
@admin_required
def user_ban(request, user_id):
    """Бан пользователя: выбор срока (День/Неделя/Месяц/Навсегда) +
    причина. 'forever' сохраняет banned_until=None, что означает бессрочный бан."""
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        duration = request.POST.get('duration', 'day')
        reason = request.POST.get('reason', '').strip()
        if duration not in BAN_DURATIONS:
            return _error_page(request, 'Неверный срок бана.')
        label, delta = BAN_DURATIONS[duration]
        banned_until = None if delta is None else timezone.now() + delta
        UserBan.objects.update_or_create(
            user=user, defaults={'banned_until': banned_until, 'reason': reason},
        )
        return redirect('admin_users')
    context = {'object_label': user.username, 'durations': BAN_DURATIONS}
    return render(request, 'portal/user_ban.html', context)


@login_required(login_url='portal_login')
@admin_required
def user_unban(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    UserBan.objects.filter(user=user).delete()
    return redirect('admin_users')


# --------------------------------------------------------------------------
# Админ-панель: комментарии
# Соответствует пункту «Администратор может удалять комментарии
# пользователей».
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def comments(request):
    items = Comment.objects.select_related('article', 'author').all()
    return render(request, 'portal/comment_list.html', {'items': items})


@login_required(login_url='portal_login')
@admin_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('admin_comments')
    return render(request, 'portal/confirm_delete.html', {
        'object_label': f'Комментарий «{comment.text[:40]}»', 'url': request.get_full_path(),
    })


# --------------------------------------------------------------------------
# Админ-панель: настройки оформления
# Соответствует пункту «Администратор может менять цвет фона проекта,
# цвет шрифта, изменять размер шрифта». Сохранение в SiteSettings,
# применение — через ThemeMiddleware.
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def settings_view(request):
    """Смена оформления: цвет фона, цвет шрифта, размер шрифта.
    Данные сохраняются в единственную запись SiteSettings (id=1)."""
    settings = SiteSettings.get_solo()
    if request.method == 'POST':
        settings.background_color = request.POST.get('background_color', settings.background_color)
        settings.font_color = request.POST.get('font_color', settings.font_color)
        settings.font_size = request.POST.get('font_size', settings.font_size)
        settings.save()
        return redirect('admin_settings')
    return render(request, 'portal/settings.html', {'settings': settings})


# --------------------------------------------------------------------------
# Админ-панель: статистика
# Соответствует пункту «Администратор может просматривать статистику»:
#   • рейтинг статей по количеству просмотров,
#   • рейтинг статей по количеству комментариев,
#   • рейтинг статей по количеству сохранений для дальнейшего прочтения.
# Три отдельных рейтинга строятся сортировкой по аннотированным счётчикам.
# --------------------------------------------------------------------------

@login_required(login_url='portal_login')
@admin_required
def stats(request):
    """Три рейтинга статей: по просмотрам, комментариям, сохранениям.
    Счётчики комментариев и сохранений получаем через annotate (Count)."""
    articles = Article.objects.annotate(
        comment_count=Count('comments', distinct=True),
        save_count=Count('saved_by', distinct=True),
    )
    by_views = articles.order_by('-views_count')
    by_comments = articles.order_by('-comment_count')
    by_saves = articles.order_by('-save_count')
    return render(request, 'portal/stats.html', {
        'by_views': by_views,
        'by_comments': by_comments,
        'by_saves': by_saves,
    })


# --------------------------------------------------------------------------
# Публичная часть портала (главная страница проекта /)
# Статьи показываются всем, но комментарии и сохранения — только
# авторизованным (иначе редирект на /login/). Просмотр на странице
# увеличивает счётчик views_count (нужен для статистики).
# --------------------------------------------------------------------------

def articles_public(request):
    items = Article.objects.filter(is_published=True).select_related('author')
    saved_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedArticle.objects.filter(user=request.user)
                         .values_list('article_id', flat=True))
    return render(request, 'portal/public_article_list.html', {
        'items': items, 'saved_ids': saved_ids,
    })


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id, is_published=True)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path(), login_url='portal_login')
        action = request.POST.get('action')
        text = request.POST.get('comment', '').strip()
        if action == 'comment' and text:
            Comment.objects.create(article=article, author=request.user, text=text)
            return redirect('article_detail', article_id=article.id)
        if action == 'save':
            SavedArticle.objects.get_or_create(user=request.user, article=article)
            return redirect('article_detail', article_id=article.id)
        if action == 'unsave':
            SavedArticle.objects.filter(user=request.user, article=article).delete()
            return redirect('article_detail', article_id=article.id)
    Article.objects.filter(pk=article.id).update(views_count=article.views_count + 1)
    article.refresh_from_db()
    comments = article.comments.select_related('author').all()
    is_saved = request.user.is_authenticated and SavedArticle.objects.filter(
        user=request.user, article=article).exists()
    return render(request, 'portal/public_article_detail.html', {
        'article': article, 'comments': comments, 'is_saved': is_saved,
    })


@login_required(login_url='portal_login')
def my_saved(request):
    saved = SavedArticle.objects.filter(user=request.user).select_related('article')
    return render(request, 'portal/my_saved.html', {'saved': saved})