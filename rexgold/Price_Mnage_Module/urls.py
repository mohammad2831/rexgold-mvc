
from django.urls import path
from . import views 

app_name ='Price_Mnage_Module'
urlpatterns = [
        #profit all
    path('profitall/add/', views.AdmiAddProfitAllView.as_view(), name='profitalladd'),
    path('profitall/<int:pk>/', views.AdminGetLastProfitAllView.as_view(), name='getlastprofitall'),
    #profit by user gruop

    path('profitusergroup/add/', views.AdmiAddProfitUserGroupView.as_view(), name='profitusergroupadd'),
    path('profitusergroup/<int:product_id>/<int:usergroup_id>/', views.AdminGetLastProfitUserGroupView.as_view(), name='getlastprofitall'),

    #profit by user
    path('profituser/add/', views.AdmiAddProfitUserView.as_view(), name='profituseradd'),
    path('profituser/<int:product_id>/<int:user_id>/', views.AdminGetLastProfitUserView.as_view(), name='getlastprofituser'),

    #config
    path('configadd/', views.AdminAddConfigPriceManageView.as_view(), name='getconfig'),
    path('configget/', views.AdminGetConfigPriceManageView.as_view(), name='getconfig'),
    
]