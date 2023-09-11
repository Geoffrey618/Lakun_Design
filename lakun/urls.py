"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
# project/urls.py
from .routing import *
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from . import routing as chat_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns
        )
    ),
})

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path('user/', include('user.urls')),
    re_path('team/', include('team.urls')),
    re_path('project/', include('project.urls')),
    re_path('chat/', include('chat.urls')),
    re_path('PrototypePage/', include('PrototypePage.urls')),
    re_path('documents/', include('documents.urls')),
    #re_path('post/', include('post.urls')),
    #re_path('source/', include('source.urls')),
    #re_path('visitor/', include('visitor.urls')),
    #re_path('comment/', include('comment.urls')),
    #re_path('admin/', include('admin.urls')),

] + websocket_urlpatterns

urlpatterns += [
                   # ... your url patterns
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
