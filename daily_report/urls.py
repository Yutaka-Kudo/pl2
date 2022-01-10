from django.urls import path

from . import views, views_no_use

app_name = "daily_report"
urlpatterns = [
    path('', views_no_use.home, name='home'),
    path('2', views.HomeTemplateView.as_view(), name='home2'),
    path('get_request', views.get_request, name='get_request'),
    path('get_request_for_create', views.get_request_for_create, name='get_request_for_create'),
    path('setup', views.setup, name='setup'),
    path('show_progress', views.show_progress, name='show_progress'),
    path('recording_bg', views.recording_bg, name='recording_bg'),
    path('create_next_file_bg', views.create_next_file_bg, name='create_next_file_bg'),
    # path('connect', views.connect, name='connect'),

]
