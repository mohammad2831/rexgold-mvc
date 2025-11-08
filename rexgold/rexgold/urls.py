
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('WXufeuLAUvDthfLDXtQVNkEKN/', admin.site.urls),
    path('',include('Home_Module.urls'),name='home'),
    path('account/',include('Account_Module.urls'),name='register'),
    path('Admin/', include('Admin_Pannel_Module.urls'), name='account'),
    path('userpanel/',include('User_Pannel_Module.urls'),name='register'),


    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),




    ]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


