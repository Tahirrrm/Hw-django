from .views import user_is_admin


def user_is_admin_processor(request):
    return {'user_is_admin': user_is_admin(request.user)}