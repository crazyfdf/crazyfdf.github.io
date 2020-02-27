from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import os
from face.face_recognition import Face_recognition
from face.face_collection import Facecollection
from nono import globalvariable
from eva.amadeus_views import index,index1,userLogin
from eva.models import UserProfile,Userinfo,Personalauthentication

path = os.path.join(settings.MEDIA_ROOT, "photo")
predictor_path = settings.MEDIA_ROOT+"/shape_predictor_68_face_landmarks.dat"
face_rec_model_path = settings.MEDIA_ROOT+"/dlib_face_recognition_resnet_model_v1.dat"
face_descriptor_path = path+"face_feature_vec.txt"
face_label_path = path+"label.txt"

face1 = Face_recognition(predictor_path, face_rec_model_path, face_descriptor_path, face_label_path)



#审查用户人脸图片
def face_verification(request):
    if not globalvariable.logined:
        return userLogin(request)
    # if globalvariable.jump:
    userstatus = UserProfile.objects.all()
    usern = {}
    imagepath = {}
    wrongimage={}
    for user in userstatus:
        if user.status == '1':
            try:
                usern[user.username] = Personalauthentication.objects.get(belong=UserProfile.objects.filter(username=user.username)[0])
                imagepath[user.username] = os.path.join(path, user.username)
                print('检查用户: {}'.format(user.username))
                wrongimage[user.username]=face1.face_verification1(imagepath[user.username])
            except Exception as e:
                pass
    # face1.face_verification1(path)
    # globalvariable.jump=False
    context={'info':wrongimage,'res':1}
    return JsonResponse(context)

# 载入人脸照片
def face_collection1(request):
    try:
        username = request.session["username"]
        path_save=os.path.join(path, username)

        if not os.path.exists(path):
            os.makedirs(path)
        Facecollection("人脸采集,按q可提前退出", 0, 10, path_save)
    except Exception as e:
        pass
    return HttpResponse("ok")

#加载人脸数据
def face_verification1(request):
    if not globalvariable.logined:
        return userLogin(request)
    userstatus = UserProfile.objects.all()
    usern = {}
    imagepath = {}
    for user in userstatus:
        if user.status == '1':
            try:
                usern[user.username] = Personalauthentication.objects.get(
                    belong=UserProfile.objects.filter(username=user.username)[0])
                imagepath[user.username] = os.path.join(path, user.username)
                print('正在载入用户: {}'.format(user.username))
                face1.face_label(imagepath[user.username],user.username)
                UserProfile.objects.filter(username=user.username).update(status=2)
            except Exception as e:
                pass
    # if not globalvariable.jump:
    #     face1.face_label(path)
    #     globalvariable.jump=True
    context = {'res': 200}
    return JsonResponse(context)

# 人脸识别登录
def face_recognition1(request):

    if not globalvariable.logined:

        label=face1.face_recognition1()

        if label !="other":
            try:
                user = UserProfile.objects.get(username=label)

                print(label)

                user.save()
                # session会话保存,username,token
                request.session['username'] = label
                request.session['token'] = user.token
                userinfo = UserProfile.objects.get(username=label)

                # 已登录
                globalvariable.logined = True
                if label == "admin":
                    return index1(request)
                context = {'info': '登陆成功', 'res': 200}
                return JsonResponse(context)


            except Exception as e:
                context = {'info': '该用户名不存在','res':2}
                pass
                return JsonResponse(context)

            return JsonResponse(context)
        else:
            context = {'info': '登录失败，请重新登录!','res':1}
            return JsonResponse(context)
    else:
        context = {'info': '登陆成功', 'res': 200}
        return JsonResponse(context)