from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from portal.models import SiteSettings

# ---------------------------------------------------------------------------
# Команда настройки административной части (запуск: python manage.py setup_admin).
# Соответствует пункту задания «Создайте группу/роль для администрирования
# портала. В неё должны входить несколько пользователей»:
#   • создаётся группа «Администраторы» (роль);
#   • в неё добавляется несколько пользователей (admin, admin2, admin3);
#   • дополнительно создаются обычные пользователи для проверки
#     комментариев, сохранений и банов;
#   • инициализируется запись SiteSettings (цвета/шрифт по умолчанию).
# ---------------------------------------------------------------------------
ADMIN_GROUP_NAME = 'Администраторы'

ADMINS = [
    {'username': 'admin', 'password': 'admin123', 'email': 'admin@example.com'},
    {'username': 'admin2', 'password': 'admin123', 'email': 'admin2@example.com'},
    {'username': 'admin3', 'password': 'admin123', 'email': 'admin3@example.com'},
]

USERS = [
    {'username': 'user1', 'password': 'user12345', 'email': 'user1@example.com'},
    {'username': 'user2', 'password': 'user12345', 'email': 'user2@example.com'},
    {'username': 'user3', 'password': 'user12345', 'email': 'user3@example.com'},
]


class Command(BaseCommand):
    help = 'Создаёт группу «Администраторы», администраторов, обычных пользователей и настройки оформления.'

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
        self.stdout.write(f'Группа «{ADMIN_GROUP_NAME}» готова.')

        for ct in ContentType.objects.all():
            if ct.app_label in ('auth', 'portal'):
                for perm in ct.permission_set.all():
                    group.permissions.add(perm)

        superuser_created = False
        for info in ADMINS:
            user, created = User.objects.get_or_create(
                username=info['username'],
                defaults={'email': info['email'], 'is_staff': True},
            )
            if created:
                user.set_password(info['password'])
                user.save()
                superuser_created = True
            group.user_set.add(user)
            self.stdout.write(self.style.SUCCESS(f'Администратор: {user.username} / {info["password"]}'))

        for info in USERS:
            user, created = User.objects.get_or_create(
                username=info['username'],
                defaults={'email': info['email']},
            )
            if created:
                user.set_password(info['password'])
                user.save()
            self.stdout.write(self.style.SUCCESS(f'Пользователь: {user.username} / {info["password"]}'))

        settings, _ = SiteSettings.objects.get_or_create(
            id=1,
            defaults={'background_color': '#f4f7f6', 'font_color': '#333333', 'font_size': '16px'},
        )
        self.stdout.write(self.style.SUCCESS(f'Настройки темы: {settings.background_color} / {settings.font_color} / {settings.font_size}'))

        self.stdout.write(self.style.WARNING('Готово. Админ-панель: /admin-panel/ (только для группы Администраторы)'))