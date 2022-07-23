from django.contrib import admin
from .models import UsersInfo

# Register your models here.
class UsersInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name',)

admin.site.register(UsersInfo, UsersInfoAdmin)
