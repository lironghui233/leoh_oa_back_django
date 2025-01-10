from rest_framework import serializers
from .models import OAUser, UserStatusChoices, OADepartment

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError('请输入正确的邮箱！')
            if not user.check_password(password):
                raise serializers.ValidationError('请输入正确的密码！')
            # 判断 user 状态
            if user.status == UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError('该用户尚未激活！')
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError('该用户已经被锁定，请联系管理员！')
            # 为了节省执行SQL语句的次数，这里我们把user直接放在attrs中，方便在视图中使用
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('请传入邮箱和密码')
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = OAUser
        exclude = ('password','groups','user_permissions')