from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.index, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
