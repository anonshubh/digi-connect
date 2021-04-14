from django.urls import path

from . import views

app_name = 'connect'

urlpatterns = [
    path('',views.index_view,name='index'),
    path('about/',views.about_view,name='about'),
    path('sectors/',views.sector_list,name='sector-list'),
    path('sector/<int:id>/<int:type_>/',views.DisplayRequest.as_view(),name='display-request'),
    path('create-request/<int:id>/',views.CreateRequest.as_view(),name='create-request'),
    path('delete-request/<int:id>/',views.request_delete,name='delete-request'),
    path('detail-request/<int:id>/',views.detailed_request_view,name='detail-request'),
    path('addremove-sender/<int:id>/',views.add_or_remove_sender_view,name='addremove-sender'),
    path('list-senders/<int:id>',views.list_senders_in_request_view,name='list-senders'),

    # API Endpoints
    path('api/list-genre/',views.genre_list_api,name='api-list-genre'),
]