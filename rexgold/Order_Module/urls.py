from django.urls import path
from . import views

urlpatterns = [

    path('list/', views.AdminAddOrderView.as_view(), name='order-list'),
    #path('add/', views.AddOrderAdminView.as_view(), name='order-add'),
]