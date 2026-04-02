from django.urls import path
from . import views

urlpatterns = [
    path('' , views.upload_page , name='upload_page'),
    path('mapping/' , views.mapping_page , name='mapping'),
    path('progress/', views.progress_page, name='progress'),
    path('data/', views.data_page, name='data'),
    path('history/', views.history_page, name='history'),
]