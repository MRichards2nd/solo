from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('success', views.success),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('create', views.create),
    path('add_record', views.add_record),
    path('view/<int:id>', views.view_record),
    path('edit/<int:id>', views.edit_record),
    path('update/<int:id>', views.update_record),
    path('delete/<int:id>', views.delete)
]