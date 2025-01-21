from rest_framework import viewsets
from .models import Inform, InformRead
from .serializers import InformSerializer, ReadInformSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Prefetch


class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer

    # 重写 get_queryset方法 筛选可见部分
    ### 通知列表可见的三种情况：
    ### 1. inform.publish = True 所有人可见
    ### 2. inform.departments 包含了用户所在部门
    ### 3. inform.author = request.user 自己发布的通知
    def get_queryset(self):
        # 多个条件的并查找，用到 Q函数
        # queryset = self.queryset.filter(Q(public=True) | Q(department=self.request.user.department) | Q(author=self.request.user))

        # 以下做法在循环中执行多次SQL语句，性能低
        # for inform in queryset:
        #     inform.is_read = InformRead.objects.filter(inform=inform, user=self.request.user).exists()
        # return queryset

        # 多个条件的并查找，用到 Q函数
        ## .select_related('author'): 这个方法用于优化数据库查询，通过它，Django会在第一次查询数据库时就加载与author字段相关联的对象。这主要用于一对一和多对一的关系，以减少数据库的查询次数，提高效率。
        ## .prefetch_related(...): 这个方法也是用于优化数据库查询的，但与select_related不同，它主要用于多对多的关系或者一对多的关系。
        ## Prefetch("reads", queryset=InformRead.objects.filter(user_id=self.request.user.uid)): 这部分指定了预加载与reads字段相关联的对象，但有一个条件：只加载那些user_id等于当前请求用户uid的InformRead对象。
        queryset = (self.queryset.select_related('author')
                    .prefetch_related(
                    Prefetch("reads", queryset=InformRead.objects.filter(user_id=self.request.user.uid))
                    ,"departments")
                    .filter(Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)).distinct())
        return queryset

    # 重写destroy，只有自己设置的inform可以删除
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == self.request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # 重写retrieve，增加统计阅读人数
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['read_count'] = InformRead.objects.filter(inform_id=instance.id).count()
        return Response(data=data)


class ReadInfromView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReadInformSerializer(data=request.data)
        if serializer.is_valid():
            inform_pk = serializer.validated_data.get("inform_pk")
            if InformRead.objects.filter(inform_id=inform_pk,  user_id=self.request.user.uid).exists():
                return Response(status=status.HTTP_200_OK)
            else:
                try:
                    InformRead.objects.create(inform_id=inform_pk, user_id=self.request.user.uid)
                except Exception as e:
                    print(e)
                    return Response(data={"detail":"阅读失败！"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': list(serializer.errors.values())}, status=status.HTTP_400_BAD_REQUEST)
