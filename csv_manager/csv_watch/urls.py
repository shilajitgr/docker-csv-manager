import rest_framework.request
from django.urls import path

from csv_watch.views.list_orders import ListOrders
from csv_watch.views.filter_orders import *

urlpatterns = [
    path('list_data/<int:page_num>/<int:page_size>', ListOrders.as_view(), name='csv-data-list'),
    path('filter_data/', FilterOrders.as_view(), name='filter-data'),
    path('export_data/', Download.as_view(), name='export-data'),
    ]
