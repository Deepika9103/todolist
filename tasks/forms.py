from django import forms
from .models import todo, User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.contrib.auth.models import User
#User=get_user_model()

#cleaned_data-> it will include a key and value for all its fields, even if the data didnt include a value for some optional fields 
#eg:- the data dict doesnt include a value for the nick_name field but cleaned_data includes its, with an empty value 

#form for creating new users. Includes all the required fields, plus a repeated password
class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    passowrd2=forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    #check that two pasowrd entries match
    def clean_password2(self):
        password = self.cleaned_data('password')
        password2 = self.cleaned_data("password2")
        if password  is not None and password!=password2:
            raise forms.ValidationError("Passwords dont match")
        return password2

    #save the provided passowrd in hashed form 
    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 

#includes all the fields on the user, but replaces field with admin's password hash display field 
class UserAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password',]

    def clean_password(self):
        return self.initial["password"]

        

class todoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['task','description','time','quote']
        #to include all the fields fields='__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
