from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.sign_in, name='signin'),
    path('signup/', views.sign_up, name='signup'),
    path('ajax/get-department/<int:university_id>/', views.get_department, name='get_department'),
    path('ajax/get-batches/<int:department_id>/', views.get_batches, name='get_batches'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-forgot-otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
