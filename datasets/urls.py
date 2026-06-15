from django.urls import path
from . import views

app_name = 'datasets'

urlpatterns = [
    path('', views.dataset_list_view, name='list'),
    path('upload/', views.dataset_upload_view, name='upload'),
    path('<int:pk>/', views.dataset_detail_view, name='detail'),
    path('<int:pk>/delete/', views.dataset_delete_view, name='delete'),
]
