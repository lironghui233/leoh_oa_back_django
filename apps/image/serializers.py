from rest_framework import serializers
from django.core.validators import FileExtensionValidator, get_available_image_extensions


class UploadImageSerializer(serializers.Serializer):
    # ImageField：会校验上传的文件是否是图片
    image = serializers.ImageField(
        # validators=[FileExtensionValidator(allowed_extensions=[get_available_image_extensions()])]
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        error_messages={'required':'请上传图片', 'invalid_image':'请上传正确格式的图片！'}
    )

    def validate_image(self, value):
        # 图片的大小是字节
        max_size = 0.5 * 1024 * 1024    #0.5MB
        size = value.size
        if size > max_size:
            raise serializers.ValidationError('图片最大不能超过0.5MB')
        return value