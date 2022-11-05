from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html #this is used to add style using html tags

#to import all models use *
# Register your models here.

#User=get_user_model()
 
#to make changes in the admin panel we need to override the admin.model class
class UserAdmin(admin.ModelAdmin):
    search_fields=['email']
    form = UserAdminChangeForm #edit view
    add_form = UserAdminCreationForm #create view

    #exclude = ('email',) -> exclude a particular field from been displayed in the admin panel, remove the mentioned fields and keep the rest fields

    list_display = ('email','admin','thisEmail',) #what u want to display in the table

    #function to display a particular thing
    def thisEmail(self, obj):
        # return 'this is an email'
        return  format_html(f'<span style="color:red">{obj.email}</span>')
        # return format_html(f'<a href="/admin/tasks/user/{obj.id}/change/">Click Here</a>')
        #use "" only if '' is used it will give an error 

    list_display_links = ('thisEmail',)

    #list_filter = (('xyz',admin.EmptyFieldListFilter),...)-> it is used to add empty as an option in the filter list, specific filter hai 
    list_filter = ('staff','admin','active',)
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

    #we can edit the attribute directly from the list view instead of going to the detail view
    # editable_list = ('thisEmail',)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    save_on_top=True # it shows save buttons on the top

    class Meta:
        model = User

class todoAdmin(admin.ModelAdmin):
    list_display = ('task','quote','description',)
    def photoTag(self,obj):
        return format_html(f'<img src="media/{obj.images}" style="height:100px;width:100px">')

admin.site.register(User, UserAdmin)
admin.site.register(todo, todoAdmin)
admin.site.register(Publication)
admin.site.register(Article)
#remove group model from admin. we are not using it 
#admin.site.unregister(Group) 
