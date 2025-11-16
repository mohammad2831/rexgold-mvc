
from django.urls import path

from . import views 
from .views import latest_prices_view
app_name = 'Product_Data_Module' 


urlpatterns = [
# --- Product URLs ---
    path('productlist/', views.AdminListProductView.as_view(), name='product_list'),
    path('productadd/', views.AdminAddProductView.as_view(), name='product_add'),
    path('productupdate/<int:pk>/', views.AdminUpdataProductView.as_view(), name='product_update'),
    path('productdetail/<int:pk>/', views.AdminDetailProductView.as_view(), name='product_detail'),
    path('productdelete/<int:pk>/', views.AdminDeleteProductView.as_view(), name='product_delete'),

    # --- Category URLs ---
    path('category/categorylist/', views.AdminListCategoryView.as_view(), name='category_list'),
    path('category/categoryadd/', views.AdminAddCategoryView.as_view(), name='category_add'),
    path('category/categoryupdate/<int:pk>/', views.AdminUpdateCategoryView.as_view(), name='category_update'),
    path('category/categorydetail/<int:pk>/', views.AdminDetailCategoryView.as_view(), name='category_detail'),
    path('category/categorydelete/<int:pk>/', views.AdminDeleteCategoryView.as_view(), name='category_delete'),


    path('price/latest-prices/', latest_prices_view, name='latest_prices'),
]