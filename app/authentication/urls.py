from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('superuser_home/', views.super_user_home_view, name='super_user_home'),
    path('regularuser_home/', views.regular_user_home_view, name='regular_user_home'),
    path('create_ticket/', views.create_ticket_view, name='create_ticket'),
    path('ticket_list/', views.ticket_list_view, name='ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status_view, name='update_ticket_status'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket_view, name='delete_ticket'),
    path('about/', views.about_view, name='about'),
]
