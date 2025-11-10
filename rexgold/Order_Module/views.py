from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
        tags=['testtt'],
       
)
class AdminAddOrderView(APIView):
    def get(self, request):
        return Response({"message": "Admin Add Order View"}, status=status.HTTP_200_OK)
