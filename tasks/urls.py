from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('',views.add,name='add'),
    path('delete/<str:pk>/',views.delete,name='delete'),
    path('update/<str:id>/',views.update,name='update')
]