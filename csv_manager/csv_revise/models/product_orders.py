from django.db import models


# Create your models here.

class ProductOrders(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_time = models.DateTimeField()
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    delivered_to_city = models.CharField(max_length=30)

    class Meta:
        ordering = ['transaction_id']
