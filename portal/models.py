from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ---------------------------------------------------------------------------
# Модели административной части портала.
# Соответствуют разделам задания:
#   • Article        — «публиковать/редактировать/удалять новости и статьи»,
#                      а также статистика «по количеству просмотров»
#   • Comment        — «удалять комментарии пользователей» + статистика
#                      «по количеству комментариев»
#   • SavedArticle   — «сохранения для дальнейшего прочтения» + статистика
#                      «по количеству сохранений»
#   • UserBan        — «банить пользователей на срок: день/неделя/месяц/навсегда»
#   • SiteSettings   — «менять цвет фона, цвет шрифта, размер шрифта»
# ---------------------------------------------------------------------------


class Article(models.Model):
    """Новость или статья, публикуемая администратором.

    • `views_count` — счётчик просмотров, используется в статистике
      «рейтинг статей по количеству просмотров».
    • `is_published` — флаг публикации: статья может быть черновиком
      (черновики не показываются на главной странице портала).
    """
    title = models.CharField('Заголовок', max_length=200)
    short_text = models.CharField('Краткое описание', max_length=500, blank=True)
    content = models.TextField('Содержание')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='articles'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    views_count = models.PositiveIntegerField('Просмотры', default=0)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def comments_count(self):
        return self.comments.count()

    def saves_count(self):
        return self.saved_by.count()


class Comment(models.Model):
    """Комментарий пользователя к статье.

    Удаляется администратором из админ-панели
    (пункт задания «удалять комментарии пользователей»).
    """
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text[:50]}'


class SavedArticle(models.Model):
    """Сохранение статьи пользователем для дальнейшего прочтения.

    Один пользователь может сохранить статью только один раз
    (`unique_together`). По количеству записей строится статистика
    «рейтинг статей по количеству сохранений».
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='saved_articles'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='saved_by'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Сохранённая статья'
        verbose_name_plural = 'Сохранённые статьи'

    def __str__(self):
        return f'{self.user} -> {self.article}'


class UserBan(models.Model):
    """Бан пользователя. banned_until=None означает «навсегда».

    Соответствует пункту «банить пользователей на какой-то срок»:
    администратор выбирает срок (день/неделя/месяц/навсегда),
    а BanMiddleware проверяет `is_active()` при каждом запросе.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='ban'
    )
    reason = models.CharField('Причина', max_length=255, blank=True)
    banned_until = models.DateTimeField(
        'До', null=True, blank=True, help_text='Пусто = навсегда'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Бан'
        verbose_name_plural = 'Баны'

    def __str__(self):
        return f'{self.user.username} до {self.banned_until}'

    @property
    def is_forever(self):
        return self.banned_until is None

    def is_active(self):
        if self.banned_until is None:
            return True
        return self.banned_until > timezone.now()


class SiteSettings(models.Model):
    """Глобальные настройки оформления портала (единственная запись).

    Соответствует пункту «менять цвет фона проекта, цвет шрифта,
    размер шрифта». Значения применяются ко ВСЕМ страницам проекта
    через ThemeMiddleware.
    """
    background_color = models.CharField('Цвет фона', max_length=20, default='#f4f7f6')
    font_color = models.CharField('Цвет шрифта', max_length=20, default='#333333')
    font_size = models.CharField('Размер шрифта', max_length=10, default='16px')

    class Meta:
        verbose_name = 'Настройка оформления'
        verbose_name_plural = 'Настройки оформления'

    def __str__(self):
        return 'Настройки оформления портала'

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)