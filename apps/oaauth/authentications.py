import jwt
import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from apps.oaauth.models import OAUser

def generate_jwt(user):
    timestamp = int(time.time()) + 60 * 60 * 24 * 7
    # timestamp = int(time.time()) + 2
    # exp 是一个特殊的参数，用于表示token过期的时间
    token = jwt.encode(
        {"user": user.uid, "exp": timestamp},
        key=settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token


class JWTAuthentication(BaseAuthentication):
    """
    请求头中：
        Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'
    model = None

    def authenticate(self, request):
        # 从请求头中获取Authorization
        # auth = ['JWT','401f7ac837da42b97f613d789819ff93537bee6a']
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = '没有提供JWT token！'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = '无效JWT!'
            raise exceptions.AuthenticationFailed(msg)

        try:
            # 解密的算法和key必须和加密的算法保持一致
            jwt_token = auth[1]
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            userid = payload.get("user")
            try:
                user = OAUser.objects.get(pk=userid)
                return (user, jwt_token)
            except Exception:
                msg = '用户信息错误！'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'UnicodeError'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = 'token已过期！'
            raise exceptions.AuthenticationFailed(msg)

