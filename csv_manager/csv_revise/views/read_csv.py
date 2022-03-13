import os

import pytz
import rest_framework
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import csv
from datetime import datetime

from csv_manager.settings import BASE_DIR
from csv_revise.models.product_orders import ProductOrders

fs = FileSystemStorage(BASE_DIR)


class ReadCSV(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        This method defines the HTTP POST mechanism to accept a csv file and persist its content in the DB.
        :param request: csv format file.
        :param args:
        :param kwargs:
        :return: Response indicating status of csv file upload operation.
        """
        if request.FILES.get("file") is None or request.FILES['file'].name is None:
            data = {
                "status": "FAILED",
                "message": "No file found"
            }
            return Response(
                data=data,
                status=rest_framework.status.HTTP_400_BAD_REQUEST
            )
        file = request.FILES.get("file")
        file_content = ContentFile(file.read())
        file_name = fs.save("new.csv", file_content)
        file_path = fs.path(file_name)

        product_order_list = []
        sid = transaction.savepoint()
        try:
            with open(file_path) as csvfile:
                csv_data = csv.reader(csvfile)
                next(csv_data)
                for id_, row in enumerate(csv_data):
                    (
                        transaction_id,
                        transaction_time,
                        product_name,
                        quantity,
                        unit_price,
                        total_price,
                        delivered_to_city
                    ) = row
                    transaction_time = datetime.strptime(transaction_time, "%Y%m%d %H%M%S").replace(tzinfo=pytz.utc)
                    # transaction_time = transaction_time.strftime("%Y%m%d %H%M%S")
                    product_order_list.append(
                        ProductOrders(
                            transaction_id=transaction_id,
                            transaction_time=transaction_time,
                            product_name=product_name,
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=total_price,
                            delivered_to_city=delivered_to_city
                        )
                    )
                csvfile.close()
            with transaction.atomic():
                ProductOrders.objects.bulk_create(product_order_list)

        except Exception as ex:
            transaction.rollback(sid)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "File is not in csv format",
                    "error": str(ex)
                },
                status=rest_framework.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        os.remove(file_path)
        return Response(
            data={
                "status": "SUCCESS",
                "message": "CSV file uploaded successfully"
            },
            status=rest_framework.status.HTTP_201_CREATED
        )
