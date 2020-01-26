from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
#用户登录



from myaifront.models import Topmenu,Banner

class TopmenuXuliehua(serializers.ModelSerializer):
    class Meta:
        depth=1
        model=Topmenu
        fields='__all__'
class BannerData(serializers.ModelSerializer):
    class Meta:
        depth=1
        model=Banner
        fields='__all__'


@api_view(['GET','POST'])
def indexData(request):
    # 首页导航栏
    topmenu=Topmenu.objects.all()
    topmenuData=TopmenuXuliehua(topmenu,many=True)
    # 首页的Banner
    banner=Banner.objects.all()
    bannerData = BannerData(banner, many=True)

    if request.method == 'POST':
        # post来的信息
        username = request.POST['username']
        password = request.POST['password']
        print('okss')
    return Response({'topmenu':topmenuData.data,'banner':bannerData.data})