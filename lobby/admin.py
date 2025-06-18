from django.contrib import admin
from .models import Session, User


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'state')
    search_fields = ('id', 'state')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'session', 'isOwner')
    search_fields = ('username',)
    list_filter = ('isOwner',)
    
    