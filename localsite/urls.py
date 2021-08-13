from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adhikari_list/<slug:meeting_type>', views.adhikari_list, name='adhikari_list'),
    path('meeting_list/<int:adhikari_id>', views.meeting_list, name='meeting_list'),
    path('import_meeting/', views.import_meeting, name='import_meeting'),
    path('import_adhikari/', views.import_adhikari, name='import_adhikari'),
    path('delete_meetings/', views.delete_meetings, name='delete_meetings'),
    path('delete_adhikari/', views.delete_adhikari, name='delete_adhikari'),
    path('update_adhikari/', views.update_adhikari, name='update_adhikari'),
    path('update_meeting/', views.update_meeting, name='update_meeting'),
    path('change_profile_image/', views.change_profile_image, name='change_profile_image'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)