from django.urls import path

from . import views, views_no_use

app_name = "display_part"
urlpatterns = [
    path('old', views_no_use.index, name='index_old'),
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('manage2', views_no_use.manage, name='manage2'),
    path('manage', views.ManageTemplateView.as_view(), name='manage'),
    path('manage_costs', views.manage_costs, name='manage_costs'),
    path('manage_manager', views.manage_manager, name='manage_manager'),

    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),

    path('detail/<str:when>', views.detailbymonth, name='detailbymonth'),
    path('detail_by_store/<str:store>/<str:when>', views.detailbystore, name='detailbystore'),
    path('detail_by_paytype/<str:kinds>', views.detailbypaytype, name='detailbypaytype'),
    # path("plot/<str:cgy>/<str:span>", views.get_svg, name="plot"),
    path("chart/<str:flg>/", views.chart, name="chart"),
    path("output_excel/<str:flag>/", views.output_excel, name="output_excel"),
]
