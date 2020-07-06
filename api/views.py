from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.response import APIResponse
from api.serializers import UserModelSerializer
from api.authentication import JWTAuthentication
# Create your views here.
from rest_framework_jwt.serializers import jwt_encode_handler
from rest_framework_jwt.serializers import jwt_payload_handler
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
