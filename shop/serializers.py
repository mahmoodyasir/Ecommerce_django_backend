from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from rest_framework.authtoken.models import Token


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {"password": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {"password": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        return user


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['prouser']

    def validate(self, attrs):
        attrs['prouser'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        depth = 3


# class ChoicesField(serializers.Field):
#     def __init__(self, choices, **kwargs):
#         self._choices = choices
#         super(ChoicesField, self).__init__(**kwargs)
#
#     def to_representation(self, obj):
#         return self._choices[obj]
#
#     def to_internal_value(self, data):
#         return getattr(self._choices, data)


class OrderSerializers(serializers.ModelSerializer):
    # order_status = ChoicesField(choices=Order.ORDER_STATUS)

    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = "__all__"


class UserExcludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('prouser',)


class WishListSerializer(serializers.ModelSerializer):
    user = UserExcludeSerializer()

    class Meta:
        model = WishList
        fields = "__all__"
        depth = 2



