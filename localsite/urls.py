from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adhikari_list/<slug:meeting_type>', views.adhikari_list, name='adhikari_list'),
    path('meeting_list/<int:adhikari_id>', views.meeting_list, name='meeting_list'),
    path('import_meeting/', views.import_meeting, name='import_meeting'),
    path('import_adhikari/', views.import_adhikari, name='import_adhikari'),
    path('delete_meetings/', views.delete_meetings, name='delete_meetings'),
    path('delete_adhikari/', views.delete_adhikari, name='delete_adhikari'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
]