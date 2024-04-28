from django.contrib import admin
from django.urls import path
from icecream import views

urlpatterns = [
    path("",views.index,name="index"),
    path("contact",views.contact,name="contact"),
    path("signup",views.signup,name="signup"),
    path("signin",views.signin,name="signin"),
    path("order",views.order,name="order")
]