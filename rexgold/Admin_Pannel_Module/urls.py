from django.urls import path ,include
from . import views, filters
from Account_Module.views import LogoutView

urlpatterns = [
    #authentication
    path('login/', views.AdminLoginGenerateOTPView.as_view(), name='login'),
    path('verify/', views.AdminVerifyOTPView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),





    #user
    path('userlist/', views.AdminListUserView.as_view(), name='userlist'),
    path('userdetail/<int:pk>/', views.AdminDetailUserView.as_view(), name='userdetail'),
    path('userdelete/<int:pk>/', views.AdminDeleteUserView.as_view(), name='userdelete'),
    path('userupdate/<int:pk>/', views.AdminUpdateUserView.as_view(), name='userupdate'),
    path('useradd/', views.AdminAddUserView.as_view(), name='useradd'),

    path('serch/users/', views.UserViewSet.as_view({'get': 'list'}), name='user-list'),


    #user-group
    path('usergroupadd/', views.AdminAddUserGroupView.as_view(), name='usergroupadd'),  
    path('usergrouplist/', views.AdminListUserGroupView.as_view(), name='usergrouplist'),
    path('usergroupdelete/<int:pk>/', views.AdminDeleteUserGroupView.as_view(), name='usergroupdelete'),
    #path('usergroupupdate/<int:pk>/', views.AdminUpdateUserGroupView.as_view(), name='usergroupupdate'),
    path('usergroupdetail/<int:pk>/', views.AdminDetailUserGroupView().as_view(), name='usergroupdetail'),




    path('order/', include('Order_Module.urls')),
    path('profit/', include('Price_Mnage_Module.urls', namespace='profit')), 
    
    path('product/', include('Product_Data_Module.urls', namespace='product')),
    path('user/', include('Account_Module.urls', namespace='Account_Module'))
    
 



]

