from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.index, name='home'),
    path("registration", views.registration, name='registration'),
    path("autorization", views.autorization, name='autorization'),
    path("logout", views.logout, name='logout'),
    path("profile", views.profile, name='profile'),
    path("add_ad", views.add_ad, name='add_ad'),
    path('ad/<int:ad_id>/', views.current_ad, name='current_ad'),
    path("category/<str:category>/", views.index, name='category'),
    path('ad/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ad/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('exchange-proposals/', views.exchange_proposals, name='exchange_proposals'),
    path('proposal/<int:proposal_id>/update/<str:status>/', views.update_proposal, name='update_proposal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
