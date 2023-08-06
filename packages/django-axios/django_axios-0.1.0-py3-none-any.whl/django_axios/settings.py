from django.conf import settings

DJANGO_AXIOS_SETTINGS = 'DJANGO_AXIOS'

DEFAULTS = {
    'socket': None
}

USER_SETTINGS = getattr(settings, DJANGO_AXIOS_SETTINGS, DEFAULTS)

SOCKET_INSTANCE = USER_SETTINGS.get('socket')
