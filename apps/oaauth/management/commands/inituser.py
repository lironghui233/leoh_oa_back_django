from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser, OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):

        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')

        # 董事会: 都是superuser用户
        # leoh：董事会 leader
        leoh = OAUser.objects.create_superuser(email='leoh@qq.com', realname="leoh", password='123123123', department=boarder)
        # 多多：董事会
        duoduo = OAUser.objects.create_superuser(email="duoduo@qq.com", realname="多多", password='111111', department=boarder)
        # 产品开发部 leader
        zhangsan = OAUser.objects.create_user(email='zhangsan@qq.com', realname="张三", password='111111', department=developer)
        # 运营部 leader
        lisi = OAUser.objects.create_user(email='lisi@qq.com', realname="李四", password='111111', department=operator)
        # 人事部 leader
        wangwu = OAUser.objects.create_user(email='wangwu@qq.com', realname="王五", password='111111', department=hr)
        # 财务部 leader
        zhaoliu = OAUser.objects.create_user(email='zhaoliu@qq.com', realname="赵六", password='111111', department=finance)
        # 销售部 leader
        sunqi = OAUser.objects.create_user(email='sunqi@qq.com', realname="孙七", password='111111', department=saler)

        # 给部门指定 leader 和 manager
        # 1. 董事会
        boarder.leader = leoh
        boarder.manager = None
        # 2. 产品开发部
        developer.leader = zhangsan
        developer.manager = leoh
        # 3. 运营部
        operator.leader = lisi
        operator.manager = leoh
        # 4. 销售部
        saler.leader = sunqi
        saler.manager = leoh
        # 5. 人事部
        hr.leader = wangwu
        hr.manager = duoduo
        # 6. 财务部
        finance.leader = zhaoliu
        finance.manager = duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write('初始用户创建成功！')