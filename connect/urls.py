from django.urls import path

from . import views

app_name = 'connect'

urlpatterns = [
    path('',views.index_view,name='index'),
    path('about/',views.about_view,name='about'),
    path('sectors/',views.sector_list,name='sector-list'),
    path('sector/<int:id>/',views.DisplayRequest.as_view(),name='display-request'),
    path('create-request/<int:id>/',views.CreateRequest.as_view(),name='create-request'),
]