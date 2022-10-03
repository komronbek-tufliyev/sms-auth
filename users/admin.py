from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'full_name', 'eskiz_id', 'key', 'eskiz_code', 'is_verified', 'is_deleted']

    
