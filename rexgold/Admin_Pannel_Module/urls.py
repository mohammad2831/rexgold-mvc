from django.urls import path ,include
from . import views, filters
from Account_Module.views import LogoutView

urlpatterns = [
    #authentication
    path('login/', views.AdminLoginGenerateOTPView.as_view(), name='login'),
    path('verify/', views.AdminVerifyOTPView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),


    #product
    path('productlist/',views.AdminListProductView.as_view(), name='productList'),
    path('productadd/', views.AdminAddProductView.as_view(), name='AddProduct'),
    path('productupdate/<int:pk>/', views.AdminUpdataProductView.as_view(), name='productupdate'),
    path('productdetail/<int:pk>/', views.AdminDetailProductView.as_view(), name='productdetail'),
    path('productdelete/<int:pk>/', views.AdminDeleteProductView.as_view(), name='DeleteProduct'),

    #category
    path('categoryadd/', views.AdminAddCategoryView.as_view(), name='categoryadd'),
    path('categorydelete/<int:pk>/', views.AdminDeleteCategoryView.as_view(), name='categorydelete'),
    path('categoryupdate/<int:pk>/', views.AdminUpdateCategoryView.as_view(), name='categoryudate'),
    path('categorydetail/<int:pk>/', views.AdminDetailCategoryView.as_view(), name='categorydetail'),
    path('categorylist/',views.AdminListCategoryView.as_view(), name='categorylist'),


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


    #profit all
    path('profitall/add/', views.AdmiAddProfitAllView.as_view(), name='profitalladd'),
    path('profitall/<int:pk>/', views.AdminGetLastProfitAllView.as_view(), name='getlastprofitall'),
    #profit by user gruop

    path('profitusergroup/add/', views.AdmiAddProfitUserGroupView.as_view(), name='profitusergroupadd'),
    path('profitusergroup/<int:product_id>/<int:usergroup_id>/', views.AdminGetLastProfitUserGroupView.as_view(), name='getlastprofitall'),

    #profit by user
    path('profituser/add/', views.AdmiAddProfitUserView.as_view(), name='profituseradd'),
    path('profituser/<int:product_id>/<int:user_id>/', views.AdminGetLastProfitUserView.as_view(), name='getlastprofituser'),



]

