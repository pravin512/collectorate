from django.contrib import admin
from localsite.models import *

# Register your models here.

class AdhikariListAdmin(admin.ModelAdmin):
    pass

class MeetingDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(AdhikariList, AdhikariListAdmin)
admin.site.register(MeetingDetails, MeetingDetailsAdmin)
