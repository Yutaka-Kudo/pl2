from django.urls import path

from . import views

app_name = "upload_part"
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin_scr, name='admin_scr'),
    path('excel_up/', views.excel_up, name='excel_up'),
    path('sheetname/', views.show_sheetname, name='show_sheetname'),

]
