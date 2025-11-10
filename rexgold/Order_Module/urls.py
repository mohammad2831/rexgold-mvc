from django.urls import path
from . import views

urlpatterns = [

    path('orderadd/', views.AdminAddOrderView.as_view(), name='order-add'),
    path('orderlist/', views.AdminListOrderView.as_view(), name='order-list'),
    path('serch/orders/', views.OrderViewSet.as_view({'get': 'list'}), name='order-list'),
   # path(''),
]