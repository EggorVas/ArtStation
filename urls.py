from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.art_list, name='art_list'),
    path('art/<int:pk>/', views.art_detail, name='art_detail'),
    path('art/new/', views.art_new, name='art_new'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
