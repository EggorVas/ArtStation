from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.art_list, name='art_list'),
    path('art/<int:pk>/', views.art_detail, name='art_detail'),
    path('art/new/', views.art_new, name='art_new'),
    path('art/<int:pk>/edit/', views.art_edit, name='art_edit'),
    path('art/<int:pk>/delete/', views.art_delete, name='art_delete'),
    path('art/favorites/', views.art_favorites, name='art_favorites'),
    path('art/favorite/<int:pk>/', views.new_art_favorite, name='new_art_favorite'),
    path('log_in/', views.log_in, name='log_in'),
    path('registration/', views.registration, name='registration'),
    path('log_out/', views.log_out, name='log_out'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
