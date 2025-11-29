
from django.urls import path
from . import views 

urlpatterns = [
    #path('orderlist/', views.AdminListUserView.as_view(), name='userlist'),
    path('orderadd/', views.UserAddOrderView.as_view(), name='updateuser'),
    
]