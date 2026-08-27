from django.shortcuts import redirect
from .models import SiteSettings


# ---------------------------------------------------------------------------
# Middleware административной части.
#   • ThemeMiddleware — «менять цвет фона / шрифта / размер шрифта»:
#     подставляет CSS-стили из SiteSettings во все HTML-ответы проекта.
#   • BanMiddleware   — «банить пользователей на срок»: не пускает
#     забаненных в любые разделы, кроме /login/, /logout/ и /ban/ (бан-станица).
# ---------------------------------------------------------------------------


class ThemeMiddleware:
    """Внедряет глобальные настройки оформления (фон, цвет шрифта, размер)
    во все HTML-ответы проекта."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        content_type = response.get('Content-Type', '')
        if 'text/html' in content_type:
            settings = SiteSettings.get_solo()
            css = (
                '<style id="portal-theme">'
                f'body {{ background-color: {settings.background_color} !important; '
                f'color: {settings.font_color} !important; '
                f'font-size: {settings.font_size} !important; }}'
                f'h1 {{ color: {settings.font_color} !important; }}'
                '</style>'
            )
            try:
                content = response.content.decode('utf-8', errors='ignore')
            except Exception:
                content = ''
            if '</head>' in content:
                content = content.replace('</head>', css + '</head>', 1)
            elif '</body>' in content:
                content = content.replace('</body>', css + '</body>', 1)
            elif content:
                content = content + css
            try:
                response.content = content.encode('utf-8')
            except Exception:
                pass
        return response


class BanMiddleware:
    """Блокирует доступ забаненным пользователям к порталу.

    Проверяются только авторизованные пользователи: если у них есть
    активный бан (UserBan), запрос перенаправляется на страницу /ban/,
    где показана причина и срок бана.
    """

    # пути, доступные забаненным пользователям
    ALLOWED_PATHS = (
        '/login/',
        '/logout/',
        '/ban/',
        '/static/',
        '/admin/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            path = request.path
            if not any(path.startswith(p) for p in self.ALLOWED_PATHS):
                ban = getattr(user, 'ban', None)
                if ban is not None and ban.is_active():
                    return redirect('ban_status')
        return self.get_response(request)