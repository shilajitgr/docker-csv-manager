from django.urls import path

from csv_revise.views.read_csv import ReadCSV
from csv_revise.views.update_data import *

urlpatterns = [
    path('upload_csv/', ReadCSV.as_view(), name='csv-upload'),
    path('update/<int:transaction_id>', UpdateRecord.as_view(), name='update-data'),
    path('remove/<int:transaction_id>', UpdateRecord.as_view(), name='delete-data'),
    ]
