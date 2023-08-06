import importlib
from typing import List, Callable

from django.db.models import Model
from django.http import HttpRequest
from django.dispatch import receiver
from django.db.models.signals import ModelSignal

from socketio import Server

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer

from .settings import SOCKET_INSTANCE

if SOCKET_INSTANCE:
    module = importlib.import_module(SOCKET_INSTANCE)
    sio = getattr(module, 'sio')
else:
    sio = Server()

Callback = Callable[[Model, Serializer, Server, bool], None]


class AxiosInstance:
    """
        Axios model instance
    """

    def __init__(self, signal: ModelSignal | List[ModelSignal], sender: Model, serializer: Serializer, callback: Callback):
        self.signal = signal
        self.sender = sender
        self.callback = callback
        self.serializer = serializer


axios_instances: List[AxiosInstance] = []


def event(signal: ModelSignal, sender: Model, serializer: Serializer = None):
    """
        register model signal
    """
    def _decorator(callback: Callback):
        axios_instances.append(AxiosInstance(
            signal, sender, serializer, callback))

    return _decorator


def http(methods: List[str]):
    """
        register api_views
    """
    def _decorator(callback: Callable[[HttpRequest, Server], Response]):
        @api_view(methods)
        def on_request(request: HttpRequest):
            return callback(request, sio)

        return on_request

    return _decorator


def init_signal(signal, sender, serializer, callback):
    """
        init model signal
    """
    @receiver(signal, sender=sender)
    def on_signal(instance: Model, created: bool, **_kwargs):
        callback(instance, serializer, sio, created)


def ready():
    """
        setup signals on django app ready
    """
    for instance in axios_instances:
        if isinstance(instance.signal) in (list, tuple):
            for signal in instance.signal:
                init_signal(signal, instance.sender,
                            instance.serializer, instance.callback)
        else:
            init_signal(instance.signal, instance.sender,
                        instance.serializer, instance.callback)
