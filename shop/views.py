from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, views
from rest_framework.response import Response

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User


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
            response_msg = {"error": True,"message": "User Data is not update !! Try Again ...."}
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