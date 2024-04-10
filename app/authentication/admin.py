from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from .models import Ticket

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'password1', 'password2', 'is_admin',),
        }),
    )
    list_display = ('email', 'is_admin',)
    list_filter = ('is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_at', 'updated_at', 'created_by')

# Register your models here
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Ticket, TicketAdmin)
