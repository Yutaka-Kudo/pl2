from django.urls import path

from . import views

app_name = "ubiregi_checker"
urlpatterns = [
    path('', views.delete_and_cancel_checker, name='delete_and_cancel_checker'),

]
