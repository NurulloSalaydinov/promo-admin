from rest_framework import serializers
from common.models import Product, Promo, Category
from clients.models import Client, Order, Visitor



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = '__all__'

