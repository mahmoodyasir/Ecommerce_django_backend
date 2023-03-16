from django.urls import path, include
from rest_framework import routers
from .views import *
from .views import sslc_status, sslc_complete

route = routers.DefaultRouter()
route.register("category", CategoryView, basename="CategoryView")
route.register("cart", MyCart, basename="cart")
route.register("orders", OldOrders, basename="orders")
route.register("any_user_order", AnyUserOrder, basename="any_user_order")
route.register("all_order", AllOrderView, basename="all_order")
route.register("get_choice", GetChoice, basename="get_choice")
route.register("product_delete", AdminDeleteProduct, basename="product_delete")
route.register("incomplete_order", IncompleteOrder, basename="incomplete_order")


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
    path('add_category/', AddCategory.as_view(), name="add_category"),
    path('delete_category/', DeleteCategory.as_view(), name="delete_category"),
    path('add_product/', AddProduct.as_view(), name="add_product"),
    path('data_count/', DataCount.as_view(), name="data_count"),
    path('admin_user/', AdminRegister.as_view(), name="admin_user"),
    path('delete_admin_user/', DeleteAdminUser.as_view(), name="delete_admin_user"),
    path('change_password/', ChangePassword.as_view(), name="change_password"),
    path('user_profile/', UserProfileView.as_view(), name="user_profile"),
    path('search_product/', NoPaginationProduct.as_view(), name="search_product"),
    path('demo_response/', DemoResponse.as_view(), name="demo_response"),
    path('checkproduct/', AlreadyAddedProductResponse.as_view(), name="checkproduct"),

    path('online_payment/', OnlinePayment.as_view(), name="online_payment"),

    path('sslc/status/', sslc_status, name='status'),
    path('sslc/complete/<val_id>/<tran_id>/<value_a>/<value_b>/<value_c>/<value_d>/', sslc_complete, name='sslc_complete'),
    # path('incomplete_order/', IncompleteOrder.as_view(), name="incomplete_order"),

]
