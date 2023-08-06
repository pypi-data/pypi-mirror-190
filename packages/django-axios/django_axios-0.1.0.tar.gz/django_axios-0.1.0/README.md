# Django Axios
emit events from django views or django database changes via python-socketio 

```shell
    pip install django-axios
```

# Usage 
in your wsgi.py or asgi.py file add this at the bottom of your file 

```python
    ...

    from socketio import WSGIApp

    from django_axios.socket import sio

    application = WSGIApp(sio, application)
```

Note: make sure to add it to the very bottom of the file to prevent unexpected behavior

# Signals 
listen to database changes using the event decorator 

```python
    from django.db.models.signal import post_save

    from django_socket.socket import event

    @event(signal, sender, serializer)
    def on_model_save(instance, serializer, socket, created):
        # your code
```

# Requests 
emit socketio event from api_view / http view

```python 
    from django_socket.socket import http

    @http(methods)
    def webhook(request, socket):
        # your code
```

# incase you have custom socketio instance initiated 

```python
    # demo/instance.py

    from socketio import Server 

    # variable name must be sio or an exception will be raised
    sio = Server(async_mode="threading")
```

in your settings.py
```python
    DJANGO_AXIOS = {
        'socket': 'demo.instance'
    }
```

# Documentation
Documentation for the current version of Bulk  is available from github README.


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lyonkvalid)