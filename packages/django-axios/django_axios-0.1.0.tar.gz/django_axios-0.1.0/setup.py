# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_axios']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-axios',
    'version': '0.1.0',
    'description': 'emit events from django views or django database changes via python-socketio',
    'long_description': '# Django Axios\nemit events from django views or django database changes via python-socketio \n\n```shell\n    pip install django-axios\n```\n\n# Usage \nin your wsgi.py or asgi.py file add this at the bottom of your file \n\n```python\n    ...\n\n    from socketio import WSGIApp\n\n    from django_axios.socket import sio\n\n    application = WSGIApp(sio, application)\n```\n\nNote: make sure to add it to the very bottom of the file to prevent unexpected behavior\n\n# Signals \nlisten to database changes using the event decorator \n\n```python\n    from django.db.models.signal import post_save\n\n    from django_socket.socket import event\n\n    @event(signal, sender, serializer)\n    def on_model_save(instance, serializer, socket, created):\n        # your code\n```\n\n# Requests \nemit socketio event from api_view / http view\n\n```python \n    from django_socket.socket import http\n\n    @http(methods)\n    def webhook(request, socket):\n        # your code\n```\n\n# incase you have custom socketio instance initiated \n\n```python\n    # demo/instance.py\n\n    from socketio import Server \n\n    # variable name must be sio or an exception will be raised\n    sio = Server(async_mode="threading")\n```\n\nin your settings.py\n```python\n    DJANGO_AXIOS = {\n        \'socket\': \'demo.instance\'\n    }\n```\n\n# Documentation\nDocumentation for the current version of Bulk  is available from github README.\n\n\n[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lyonkvalid)',
    'author': 'Oguntunde Caleb',
    'author_email': 'usegong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
