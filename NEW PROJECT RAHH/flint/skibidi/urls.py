from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_donor/', views.register_donor, name='register_donor'),
    path('donor_login/', views.donor_login, name='donor_login'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('update/', views.update_donor, name='update_donor'),
    path('donor_logout/', views.donor_logout, name='donor_logout'),
    path('register_receiver/', views.receiver_register, name='register_receiver'),
    path('receiver_login/', views.receiver_login, name='receiver_login'),
    path('receiver_dashboard/', views.receiver_dashboard, name='receiver_dashboard'),
    path('receiver_logout/', views.receiver_logout, name='receiver_logout'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),

    

]