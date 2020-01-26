from django.urls import path
from eva import amadeus_views
from eva import amadeus_admin

urlpatterns = [
    # 主页
    path('', amadeus_views.index),
    # 登录
    path('userLogin', amadeus_views.userLogin),
    # 人脸识别登录
    path('userLogin1', amadeus_views.userLogin1),
    # 个人信息
    path('personalinformation', amadeus_views.personalinformation),
    # 注册
    path('userregistration', amadeus_views.userregistration),
    # 404
    path('404', amadeus_views.page404),
    # 登出
    path('userlogout', amadeus_views.userlogout),
    # 实名认证
    path('authentication', amadeus_views.authentication),
    #审查用户人脸图片
    path('face_verification', amadeus_admin.face_verification),
    #加载人脸数据
    path('face_verification1', amadeus_admin.face_verification1),
    #管理员主页
    path('admin_index', amadeus_admin.index1),
    # 人脸识别
    path('face_recognition1', amadeus_admin.face_recognition1),
    # 载入人脸照片
    path('face_collection1', amadeus_admin.face_collection1),
    # AI交流
    path('ai', amadeus_views.ai),
    # 数据分析图
    path('charts',amadeus_views.charts),
    # 地区分布条形图
    path('reptile', amadeus_views.reptile),
    # 地区分布条形图
    path('a',amadeus_views.a),
    # 地区分布条形图
    path('b', amadeus_views.b),
    # 地区分布条形图
    path('c', amadeus_views.c),
    # 地区分布条形图
    path('d', amadeus_views.d),
    # 地区分布条形图
    path('e', amadeus_views.e),
]
