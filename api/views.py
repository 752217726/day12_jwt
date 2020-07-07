from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from api.paginations import MyPageNumberPagination,LimitOffsetPagination,MyCursorPagination
from api.models import Computer
from utils.response import APIResponse
from api.serializers import UserModelSerializer, ComputerModelSerializer
from api.authentication import JWTAuthentication
# Create your views here.
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler
from api.filter import ComputerFilterSet, LimitFilter


class UserDetailAPIView(APIView):
    """
    只有登录后才可以访问
    """
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self,request,*args,**kwargs):
        return APIResponse(results={"username":request.user.username,"phone":request.user.phone,"email":request.user.email})

class LoginAPIView(APIView):
    """
    实现多方式登录签发token：账号 手机号 邮箱登录
    1.禁用权限与认证组件
    2.获取前端发送的参数
    3.校验参数得到对应的用户
    4.签发token并返回
    """
    authentication_classes = []
    permission_classes = []

    def post(self,request,*args,**kwargs):
        user_ser=UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)

        return APIResponse(data_message="ok",token=user_ser.token,results=UserModelSerializer(user_ser.obj).data)

class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class =ComputerModelSerializer

    #通过此参数配置过滤的器类
    filter_backends = [SearchFilter,OrderingFilter,LimitFilter,DjangoFilterBackend]
    #指定当前搜索条件
    search_fields=["name","price"]  #url/？search=要搜索的名字

    #排序
    ordering=["price"]


    #指定分页器  不能使用列表或者元组指定
    # pagination_class =MyPageNumberPagination
    # pagination_class=LimitOffsetPagination
    # pagination_class = MyCursorPagination

    filter_class=ComputerFilterSet