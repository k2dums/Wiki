from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("new_page",views.new_page,name="new_page"),
    path("edit_page",views.edit_page,name="edit_page"),
    path("<str:title>",views.page,name="page"),

    
]
