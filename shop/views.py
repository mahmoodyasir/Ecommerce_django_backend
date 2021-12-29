from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, views, status
from rest_framework.response import Response

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse


# Create your views here.


class ProductView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializers
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)


class CategoryView(viewsets.ViewSet):
    def list(self, request):
        query = Category.objects.all().order_by("-id")
        serializers = CategorySerializer(query, many=True)
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        query = Category.objects.get(id=pk)
        serializers = CategorySerializer(query)
        serializers_data = serializers.data
        all_data = []
        category_products = Product.objects.filter(category_id=serializers_data['id'])
        category_products_serializer = ProductSerializers(category_products, many=True)
        serializers_data["category_products"] = category_products_serializer.data
        all_data.append(serializers_data)
        return Response(all_data)


class ProfileView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            query = Profile.objects.get(prouser=request.user)
            serializer = ProfileSerializers(query)
            response_msg = {"error": False, "data": serializer.data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class UserDataUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            data = request.data

            # print(user, " $$$$$$ Requested User")
            # print(data["first_name"])
            # print(data["last_name"])
            # print(data["email"])

            user_obj = User.objects.get(username=user)
            # print(user_obj)
            user_obj.first_name = data["first_name"]
            user_obj.last_name = data["last_name"]
            user_obj.email = data["email"]
            user_obj.save()

            response_msg = {"error": False, "message": "User Data is Updated"}
        except:
            response_msg = {"error": True, "message": "User Data is not update !! Try Again ...."}
        return Response(response_msg)


class ProfileImageUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            query = Profile.objects.get(prouser=user)

            serializers = ProfileSerializers(query, data=data, context={"request": request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            response_msg = {"error": False, "message": "Profile Image Updated !!"}
        except:
            response_msg = {"error": True, "message": "Profile Image not Update !! Try Again ...."}
        return Response(response_msg)


class MyCart(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers = CartSerializers(query, many=True)
        all_data = []
        for cart in serializers.data:
            cart_product = CartProduct.objects.filter(cart=cart['id'])
            cart_product_serializer = CartProductSerializers(cart_product, many=True)
            cart["cartproduct"] = cart_product_serializer.data
            all_data.append(cart)
        return Response(all_data)


class OldOrders(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        query = Order.objects.filter(cart__customer=request.user.profile)

        # temp = request.user.profile.prouser.id
        # user = Profile.objects.get(prouser_id=temp)
        # print(user)

        serializers = OrderSerializers(query, many=True)
        all_data = []
        for order in serializers.data:
            cart_product = CartProduct.objects.filter(cart_id=order['cart']['id'])
            cart_product_serializer = CartProductSerializers(cart_product, many=True)
            order['cartproduct'] = cart_product_serializer.data
            all_data.append(order)
        return Response(all_data)

    def retrieve(self, request, pk=None):
        try:
            query = Order.objects.get(id=pk)
            serializers = OrderSerializers(query)
            data = serializers.data
            all_data = []
            cartproduct = CartProduct.objects.filter(cart_id=data['cart']['id'])
            cartproduct_serializer = CartProductSerializers(cartproduct, many=True)
            data["cartproduct"] = cartproduct_serializer.data
            all_data.append(data)
            response_msg = {'err': False, "data": all_data}
        except:
            response_msg = {'err': True, "data": "No Data Found !! "}
        return Response(response_msg)

    def create(self, request):
        try:
            data = request.data
            cart_id = data['cartId']
            address = data['address']
            email = data['email']
            mobile = data['mobile']
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.complete = True
            cart_obj.save()
            Order.objects.create(
                cart=cart_obj,
                address=address,
                mobile=mobile,
                email=email,
                total=cart_obj.total,
                discount=0
            )
            response_msg = {"error": False, "message": "Your order is complete"}
        except:
            response_msg = {"error": True, "message": "Something is wrong ! "}

        return Response(response_msg)

    def destroy(self, request, pk=None):
        try:
            order_obj = Order.objects.get(id=pk)
            cart_obj = Cart.objects.get(id=order_obj.cart.id)
            order_obj.delete()
            cart_obj.delete()
            response_msg = {"error": False, "message": "Order is deleted"}
        except:
            response_msg = {"error": True, "message": "Something is wrong !!"}

        return Response(response_msg)


class AddtoCart(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        product_id = request.data['id']
        product_obj = Product.objects.get(id=product_id)
        cart_cart = Cart.objects.filter(customer=request.user.profile).filter(complete=False).first()
        cart_product_obj = CartProduct.objects.filter(product__id=product_id).first()

        try:
            if cart_cart:
                print("OLD CART")
                this_product_in_cart = cart_cart.cartproduct_set.filter(product=product_obj)
                if this_product_in_cart.exists():
                    cart_product_uct = CartProduct.objects.filter(product=product_obj).filter(
                        cart__complete=False).first()
                    cart_product_uct.quantity += 1
                    cart_product_uct.subtotal += product_obj.selling_price
                    cart_product_uct.save()
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
                else:
                    cart_product_new = CartProduct.objects.create(
                        cart=cart_cart,
                        price=product_obj.selling_price,
                        quantity=1,
                        subtotal=product_obj.selling_price
                    )
                    cart_product_new.product.add(product_obj)
                    cart_cart.total += product_obj.selling_price
                    cart_cart.save()
            else:
                print("NEW CART")
                Cart.objects.create(
                    customer=request.user.profile,
                    total=0,
                    complete=False
                )
                new_cart = Cart.objects.filter(customer=request.user.profile).filter(complete=False).first()
                cart_product_new = CartProduct.objects.create(
                    cart=new_cart,
                    price=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price
                )
                cart_product_new.product.add(product_obj)
                new_cart.total += product_obj.selling_price
                new_cart.save()
            response_msg = {"error": False, "message": "Product is added to cart"}

        except:
            response_msg = {"error": True, "message": "Product is not added to cart !! Try Again"}

        return Response(response_msg)


class IncreaseCart(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cart_product_id = request.data["id"]
        cart_product = CartProduct.objects.get(id=cart_product_id)
        cart_obj = cart_product.cart

        cart_product.quantity += 1
        cart_product.subtotal += cart_product.price
        cart_product.save()

        cart_obj.total += cart_product.price
        cart_obj.save()

        return Response({"message": "Cart Product is Added"})


class DecreaseCart(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cart_product_id = request.data["id"]
        cart_product = CartProduct.objects.get(id=cart_product_id)
        cart_obj = cart_product.cart

        cart_product.quantity -= 1
        cart_product.subtotal -= cart_product.price
        cart_product.save()

        if cart_product.quantity==0:
            cart_product.delete()

        cart_obj.total -= cart_product.price
        cart_obj.save()

        return Response({"message": "Cart Product is Decreased"})


class DeleteCartProduct(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        cart_product = CartProduct.objects.get(id=request.data['id'])
        cart_product.delete()

        return Response({"message": "cart Product is deleted"})


class DeleteFullCart(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        try:
            cart_id = request.data['id']
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.delete()
            response_msg = {"error": False, "message": "cart is Deleted"}
        except:
            response_msg = {"error": False, "message": "cart is Deleted"}

        return Response(response_msg)


class RegisterView(views.APIView):
    def post(self, request):
        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": f"User is created for '{serializers.data['username']}'"})
        return Response({"error": True, "message": "Something is wrong"})


# Custom_Admin_Panel_Token_Authentication

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'admin_token': token.key,
                'user_id': user.pk,
                'email': user.email,
                "message": True
            })
        else:
            return Response({"error": True, "message": False})


class AdminProfileView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        try:
            query = Profile.objects.get(prouser=request.user)
            serializer = ProfileSerializers(query)
            response_msg = {"error": False, "data": serializer.data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class AddCategory(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        serializers = CategorySerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": "Category is Added"})
        return Response({"error": True, "message": "Something is wrong"})


class DeleteCategory(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        category_product = Category.objects.get(id=request.data['id'])
        category_product.delete()

        return Response({"message": "Category Product is deleted"})


class AddProduct(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        data = request.data
        serializers = ProductSerializers(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            cat_id = data["category"]
            serializers.save()
            pro_obj = Product.objects.last()
            pro_obj.category = Category.objects.get(id=cat_id)
            pro_obj.save()

            return Response({"error": False, "message": "Product is Added"})
        return Response({"error": True, "message": "Something is wrong"})


class AllOrderView(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAdminUser, ]

    def list(self, request):
        queryset = Order.objects.all().order_by("-id")
        serializers = OrderSerializers(queryset, many=True)
        all_data = []

        for all_order in serializers.data:
            cart_product = CartProduct.objects.filter(cart_id=all_order['cart']['id'])
            cart_product_serializer = CartProductSerializers(cart_product, many=True)
            all_order['cartproduct'] = cart_product_serializer.data

            user_queryset = User.objects.filter(profile__cart=all_order['cart']['id'])
            user_serializer = UserSerializer(user_queryset, many=True)
            all_order['userdata'] = user_serializer.data

            Profile_queryset = Profile.objects.filter(cart=all_order['cart']['id'])
            Profile_queryset_serializer = ProfileSerializers(Profile_queryset, many=True)
            all_order['profile_user'] = Profile_queryset_serializer.data

            all_data.append(all_order)

        return Response(all_data)

    def retrieve(self, request, pk=None):
        try:
            query = Order.objects.get(id=pk)
            serializers = OrderSerializers(query)
            data = serializers.data
            all_data = []
            cart_product = CartProduct.objects.filter(cart_id=data['cart']['id'])
            cart_product_serializer = CartProductSerializers(cart_product, many=True)
            data["cartproduct"] = cart_product_serializer.data

            user_queryset = User.objects.filter(profile__cart=data['cart']['id'])
            user_serializer = UserSerializer(user_queryset, many=True)
            data['userdata'] = user_serializer.data

            Profile_queryset = Profile.objects.filter(cart=data['cart']['id'])
            Profile_queryset_serializer = ProfileSerializers(Profile_queryset, many=True)
            data['profile_user'] = Profile_queryset_serializer.data

            all_data.append(data)
            response_msg = {'err': False, "data": all_data}
        except:
            response_msg = {'err': True, "data": "No Data Found !! "}
        return Response(response_msg)

    def create(self, request):
        try:
            data = request.data
            order_id = data['id']
            payment_st = data['payment_complete']
            order_st = data['order_list']
            order_obj = Order.objects.get(id=order_id)
            print(type(order_obj))

            order_obj.order_list = Choice.objects.get(id=order_st)
            if payment_st == "true":
                order_obj.payment_complete = True
            elif payment_st == "false":
                order_obj.payment_complete = False
            order_obj.save()

            print(payment_st)
            print(order_st)

            response_msg = {"error": False, "message": "Your order is Edited"}
        except:
            response_msg = {"error": True, "message": "Something is wrong ! "}

        return Response(response_msg)


class GetChoice(viewsets.ViewSet):

    def list(self, request):
        query = Choice.objects.all().order_by("-id")
        serializers = ChoiceSerializer(query, many=True)
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        query = Choice.objects.get(id=pk)
        serializers = ChoiceSerializer(query)
        serializers_data = serializers.data
        all_data = []
        order_status = Order.objects.filter(order_list_id=serializers_data['id'])
        order_status_serializer = OrderSerializers(order_status, many=True)
        serializers_data["orders"] = order_status_serializer.data
        all_data.append(serializers_data)
        return Response(all_data)


class AnyUserOrder(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        users = Profile.objects.get(prouser_id=pk)
        print(users)

        # return Response("Testing")
        query = Order.objects.filter(cart__customer=users)

        # temp = request.user.profile.prouser.id

        serializers = OrderSerializers(query, many=True)
        all_data = []
        for order in serializers.data:
            cart_product = CartProduct.objects.filter(cart_id=order['cart']['id'])
            cart_product_serializer = CartProductSerializers(cart_product, many=True)
            order['cartproduct'] = cart_product_serializer.data
            all_data.append(order)
        return Response(all_data)


class AdminDeleteProduct(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def destroy(self, request, pk=None):
        try:
            product_obj = Product.objects.get(id=pk)
            product_obj.delete()
            response_msg = {"error": False, "message": "Product is deleted"}
        except:
            response_msg = {"error": True, "message": "Something is wrong !!"}

        return Response(response_msg)


class DataCount(views.APIView):
    def get(self, request):
        cart = Cart.objects.all().values()
        users = Profile.objects.all().values()
        profile = User.objects.all().values()
        cartproduct = CartProduct.objects.all().values()
        order = Order.objects.all().values()
        product = Product.objects.all().values()
        category = Category.objects.all().values()
        return Response({'cart': cart,
                             'users': users,
                             'profile': profile,
                         "cartproduct": cartproduct,
                         "order": order,
                         "product": product,
                         "category": category},
                             status=status.HTTP_200_OK)



