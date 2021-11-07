from django.urls import path, include
from rest_framework import routers
from .views import *

route = routers.DefaultRouter()
route.register("category", CategoryView, basename="CategoryView")
route.register("cart", MyCart, basename="cart")

urlpatterns = [
    path("", include(route.urls)),
    path('product/', ProductView.as_view(), name="product"),
    path('product/<int:id>/', ProductView.as_view(), name="product"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('userdataupdate/', UserDataUpdate.as_view(), name="userdataupdate"),
    path('profile_image_update/', ProfileImageUpdate.as_view(), name="profile_image_update"),

]
