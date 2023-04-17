from rest_framework import serializers
from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ['fio', 'email', 'password']

    def save(self, **kwargs):
        user = UserCustom(
            fio=self.validated_data['fio'],
            username=self.validated_data['fio'],
            email=self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
