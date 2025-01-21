from rest_framework.views import APIView
from .serializers import UploadImageSerializer
from rest_framework.response import Response
from rest_framework import status
from shortuuid import uuid
import os
from django.conf import settings

class UploadImageView(APIView):
    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('image')
            # 生成唯一 filename
            filename = uuid() + os.path.splitext(file.name)[-1]
            path = settings.MEDIA_ROOT / filename
            # 保存图片
            try:
                with open(path, 'wb+') as fp:
                    for chunk in file.chunks():
                        fp.write(chunk)
            except Exception:
                return Response({
                    "errno": 1, # 只要不等于 0 就行
                    "message": "失败信息",
                })
            file_url = settings.MEDIA_URL + filename
            return Response({
                "errno": 0,  # 注意：值是数字，不能是字符串
                "data": {
                    "url": file_url,   # 图片 src ，必须
                    "alt": "",   # 图片描述文字，非必须
                    "href": file_url   # 图片的链接，非必须
                }
            })
        else:
            print(serializer.errors)
            return Response({
                "errno": 1,
                "message": list(serializer.errors.values())[0][0],
            })
