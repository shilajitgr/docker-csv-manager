from rest_framework import serializers
from csv_revise.models.product_orders import ProductOrders


class ProductOrdersSerializer(serializers.ModelSerializer):
    transaction_time = serializers.DateTimeField(format="%Y%m%d %H%M%S")

    class Meta:
        model = ProductOrders
        fields = '__all__'
