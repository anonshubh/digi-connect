from django.urls import path

from . import views

app_name = 'connect'

urlpatterns = [
    path('',views.index_view,name='index'),
    path('about/',views.about_view,name='about'),
    path('policy/',views.policy_view,name='policy'),

    path('sectors/',views.sector_list,name='sector-list'),
    path('sector/<int:id>/<int:type_>/',views.DisplayRequest.as_view(),name='display-request'),
    path('create-request/<int:id>/',views.CreateRequest.as_view(),name='create-request'),
    path('delete-request/<int:id>/',views.request_delete,name='delete-request'),
    path('detail-request/<int:id>/',views.detailed_request_view,name='detail-request'),
    path('addremove-sender/<int:id>/',views.add_or_remove_sender_view,name='addremove-sender'),
    path('list-senders/<int:id>',views.list_senders_in_request_view,name='list-senders'),
    path('final-add/<int:id>/<str:username>/',views.final_accept_view,name = 'final-addremove'),
    path('view-contact-sender/<int:id>/',views.view_contact_after_match_sender,name='view-contact-sender'),
    path('view-contact-receiver/<int:id>/<str:username>/',views.view_contact_after_match_receiver,name='view-contact-receiver'),
    path('deny-request/<int:id>/<str:username>/',views.deny_request_view,name='deny-request'),
    path('pending/',views.pending_list_view,name='pending'),
    path('accepted/',views.accepted_list_view,name='accepted'),
    path('completed/',views.completed_list_view,name='completed'),

    # API Endpoints
    path('api/list-genre/',views.genre_list_api,name='api-list-genre'),
]