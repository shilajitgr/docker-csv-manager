import csv

from django.http import HttpResponse

import rest_framework
from rest_framework import generics, status
from rest_framework.response import Response

from csv_revise.models.product_orders import ProductOrders
from csv_revise.Serializer.product_orders_serializer import ProductOrdersSerializer


def filterFunc(request):
    filtered = ProductOrders.objects.all()

    not_proper = []
    if "date_range" in request.data and len(request.data["date_range"]) == 2:
        try:
            filtered = filtered.filter(transaction_time__range=request.data["date_range"])
        except Exception as ex:
            not_proper.append(f"\ndate_range {str(ex)}\n")
    else:
        not_proper.append("date_range")

    if "total_price_range" in request.data and len(request.data["total_price_range"]) == 2:
        try:
            filtered = filtered.filter(total_price__range=request.data["total_price_range"])
        except Exception as ex:
            not_proper.append(f"\ntotal_price_range {str(ex)}\n")
    else:
        not_proper.append("total_price_range")

    if "quantity_range" in request.data and len(request.data["quantity_range"]) == 2:
        try:
            filtered = filtered.filter(quantity__range=request.data["quantity_range"])
        except Exception as ex:
            not_proper.append(f"\nquantity_price_range {str(ex)}\n")
    else:
        not_proper.append("quantity_price_range")

    if "city_name" in request.data:
        try:
            filtered = filtered.filter(delivered_to_city=request.data["city_name"])
        except Exception as ex:
            not_proper.append(f"\ncity_name {str(ex)}\n")
    else:
        not_proper.append("city_name")

    return filtered, not_proper


class FilterOrders(generics.ListAPIView):
    queryset = ProductOrders.objects.all()

    def get(self, request, *args, **kwargs):

        filtered, not_proper = filterFunc(request)

        if len(filtered) == 0:
            data = {
                "status": "SUCCESS",
                "message": "No Data found for given combination of filters.",
                "product_order_details": []
            }
        else:
            data = {
                "status": "SUCCESS",
                "message": "Data filtered successfully.",
                "product_order_details": ProductOrdersSerializer(filtered, many=True).data
            }
        if not_proper:
            data["filter error"] = f"The following filter were not in proper format {not_proper} or error occured" \
                                   f" while applying them. Please check the API doc to see the correct format."

        return Response(
            data=data,
            status=rest_framework.status.HTTP_206_PARTIAL_CONTENT if "filter error" in data
            else rest_framework.status.HTTP_200_OK
        )


class Download(generics.ListAPIView):
    queryset = ProductOrders.objects.all()

    def get(self, request, *args, **kwargs):
        filtered, not_proper = filterFunc(request)
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(["transaction_id", "transaction_time", "product_name", "quantity",
                         "unit_price", "total_price", "delivered_to_city"])

        for row in filtered.values_list("transaction_id", "transaction_time", "product_name", "quantity",
                                        "unit_price", "total_price", "delivered_to_city"):
            writer.writerow(row)

        response["Content-Disposition"] = 'attachment; filename="filtered_data.csv"'

        return response
