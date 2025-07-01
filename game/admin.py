from django.contrib import admin
from .models import UserInfo, Voiting
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Voiting)
class VoitingAdmin(admin.ModelAdmin):
    pass
