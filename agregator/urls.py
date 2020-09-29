"""agregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from apps.core.views import frontpage # из apps/core/views.py
from apps.agprofile.views import get_profile
from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('', frontpage, name='frontpage'), # корневой урл, name - псевдним для шаблонов
    path('<int:site>',frontpage, name='site_news_url'),
    path ('logout/',views.LogoutView.as_view(), name='logout'),# defaulf logout view
    path ('login/',views.LoginView.as_view(template_name='core/login.html'),name='login'), # подменяем страницу логина своим шаблоном
    path ('agprofile/<str:username>/', get_profile, name = 'get_profile'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # только если debug-True