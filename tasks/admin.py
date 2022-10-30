from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import todo, User
from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#to import all models use *
# Register your models here.

#User=get_user_model()

class UserAdmin(admin.ModelAdmin):
    search_fields=['email']
    form = UserAdminChangeForm #edit view
    add_form = UserAdminCreationForm #create view

    list_display = ('email','admin',)
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',{'fields': ()}),
        ('Permissions', {'fields':('admin','staff','active',)}),
    ) 
    # add_fields is not a standard ModelAdmin attribute. UserAdmin
    # override get_fieldsets to use this attribute when creating a user 

    add_fields = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    class Meta:
        model = User

admin.site.register(User, UserAdmin)
admin.site.register(todo)
#remove group model from admin. we are not using it 
#admin.site.unregister(Group) 
