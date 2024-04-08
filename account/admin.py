from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
# from django.contrib.auth import get_user_model



class AccountAdmin(UserAdmin):
    list_display = ('pk','phone','date_joined', 'last_login','role','email', 'is_admin','is_active')
    search_fields = ('pk','phone',)
    readonly_fields=('pk', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('pk',)


admin.site.register(Account, AccountAdmin)

# class EmployeeAdmin(UserAdmin):
#     ordering = ['email', ]
#     list_display = ['pk','phone','date_joined', 'last_login','role','email', 'is_admin','is_active']
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#     #     ('Info', {'fields': ('first_name', 'last_name', 'phone',)}),
#     #     ('Address', {'fields': ('address', 'city', 'state', 'zip_code')}),
#     #     ('Schedule', {'fields': ('time_off',)}),
#     #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
#     #                                 'groups', 'user_permissions')}),
#     #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     # )
#     add_fieldsets = (
#         ("User Details", {'fields': ('email', 'password')}),
#         ("Permission", {'fields': ('is_active', 'is_staff', 'is_admin')}),
#     )


# admin.site.register(get_user_model(), EmployeeAdmin)