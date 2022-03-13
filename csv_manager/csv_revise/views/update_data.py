from datetime import datetime
import pytz

import rest_framework.status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from csv_revise.models.product_orders import ProductOrders
from csv_revise.Serializer.product_orders_serializer import ProductOrdersSerializer


class UpdateRecord(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        serializer_class = ProductOrdersSerializer()
        sid = transaction.savepoint()
        try:
            db_entry = ProductOrders.objects.get(transaction_id=kwargs["transaction_id"])
        except ObjectDoesNotExist:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "No matching entry found"
                },
                status=rest_framework.status.HTTP_204_NO_CONTENT
            )
        request.data["transaction_time"] = datetime.strptime(request.data["transaction_time"],
                                                             "%Y%m%d %H%M%S").replace(tzinfo=pytz.utc)
        try:
            with transaction.atomic():
                serializer_class.update(db_entry, request.data)
        except Exception as ex:
            transaction.rollback(sid)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Error occured while updating DB entry",
                    "error": str(ex)
                },
                status=rest_framework.status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={
                "status": "SUCCESS",
                "message": f"DB entry having transaction id={kwargs['transaction_id']} has been updated.",
            },
            status=rest_framework.status.HTTP_200_OK
        )

    def delete(self, *args, **kwargs):
        serializer_class = ProductOrdersSerializer()
        sid = transaction.savepoint()
        try:
            db_entry = ProductOrders.objects.get(transaction_id=kwargs["transaction_id"])
        except ObjectDoesNotExist:
            return Response(
                data={
                    "status": "FAILED",
                    "message": "No matching entry found"
                },
                status=rest_framework.status.HTTP_204_NO_CONTENT
            )

        try:
            with transaction.atomic():
                db_entry.delete()
        except Exception as ex:
            transaction.rollback(sid)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Error occured while deleting DB entry",
                    "error": str(ex)
                },
                status=rest_framework.status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={
                "status": "SUCCESS",
                "message": f"DB entry having transaction id={kwargs['transaction_id']} has been deleted.",
            },
            status=rest_framework.status.HTTP_200_OK
        )
