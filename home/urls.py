from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('routeen-list/', views.routeenList, name='routeenlist'),
    path('routeen/<int:pk>/', views.routeen, name='routeen'),
    path('manage-university/', views.manage_university, name='manage_university'),
    path('university/<int:university_id>/manage/', views.update_university, name='update_university'),
    path('university/', views.university_detail_view, name='university_detail_view'),
    path('routeen/create/', views.create_routeen, name='add_routeen'),
    path('routeen/<int:pk>/edit/', views.edit_routeen, name='edit_routeen'),
    path('subscribe/ajax/', views.subscribe_email_ajax, name='subscribe_ajax'),
]
