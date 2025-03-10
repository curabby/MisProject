from django.contrib import admin
from .models import Users, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'middle_name',
        'role',
        'is_admin',
        'is_staff'
    )
    list_filter = ('is_admin', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'middle_name',
                'phone',
                'role'
            )
        }),
        ('Permissions', {
            'fields': ('is_admin',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions'
                       )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'middle_name',
                'role'
            ),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
