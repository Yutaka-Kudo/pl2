from config.settings import DEBUG
from django.urls import path

from . import views

app_name = "prediction"
urlpatterns = [
    path('chart/<str:store_str>', views.show_chart, name='show_chart'),
    path('chart_long/<str:store_str>', views.show_chart_long, name='show_chart_long'),

]
