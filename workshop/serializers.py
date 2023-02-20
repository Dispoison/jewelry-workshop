from rest_framework import serializers


class CartIdSerializer(serializers.Serializer):
    id = serializers.CharField()


class CartUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    quantity = serializers.IntegerField()


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    phone_number = serializers.CharField(max_length=16)
    email = serializers.EmailField()


class OrderInfoSerializer(serializers.Serializer):
    cart = CartUpdateSerializer(many=True)
    client = ClientSerializer()
