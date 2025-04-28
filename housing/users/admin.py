from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .form import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    # Forms for adding and changing user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Fields to display in the admin list view
    list_display = ('email', 'username', 'first_name', 'last_name', 
                    'is_active', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    # Fieldsets for add/edit pages
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', )}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets for add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    # Custom actions
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users were successfully activated.")
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users were successfully deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

    # Custom list display methods
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

    # Change list view configuration
    list_per_page = 25
    list_max_show_all = 100
    show_full_result_count = True

    # Customize the user change form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            
        return form

# Register the CustomUser model with the enhanced admin class
admin.site.register(CustomUser, CustomUserAdmin)