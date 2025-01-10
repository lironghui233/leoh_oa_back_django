from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        # 1. 验证数据是否可用
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = datetime.now()
            user.save()
            # 生成 token
            token = generate_jwt(user)
            return Response({'token': token, 'user': UserSerializer(instance=user).data}, status=status.HTTP_200_OK)
        else:
            detail = list(serializer.errors.values())[0][0]
            # drf在返回响应是非200的时候，他的错误参数名叫detail
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)

