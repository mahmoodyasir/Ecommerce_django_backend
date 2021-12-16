from django.urls import path, include
from rest_framework import routers
from .views import *

route = routers.DefaultRouter()
route.register("category", CategoryView, basename="CategoryView")
route.register("cart", MyCart, basename="cart")
route.register("orders", OldOrders, basename="orders")

urlpatterns = [
    path("", include(route.urls)),
    path('product/', ProductView.as_view(), name="product"),
    path('product/<int:id>/', ProductView.as_view(), name="product"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('userdataupdate/', UserDataUpdate.as_view(), name="userdataupdate"),
    path('profile_image_update/', ProfileImageUpdate.as_view(), name="profile_image_update"),
    path('addtocart/', AddtoCart.as_view(), name="addtocart"),
    path('increasecart/', IncreaseCart.as_view(), name="increasecart"),
    path('decreasecart/', DecreaseCart.as_view(), name="decreasecart"),
    path('deletecartproduct/', DeleteCartProduct.as_view(), name="deletecartproduct"),
    path('deletefullcart/', DeleteFullCart.as_view(), name="deletefullcart"),
    path('register/', RegisterView.as_view(), name="register"),
    path('admin_login/', CustomAuthToken.as_view(), name="admin_login"),
    path('admin_profile/', AdminProfileView.as_view(), name="admin_profile"),

]
