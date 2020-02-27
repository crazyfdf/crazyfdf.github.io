#coding=UTF-8
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from eva.models import UserProfile,Userinfo,Personalauthentication
from eva.reptile import remain
import time,random,os,re
from eva.turing_test import *
from django.conf import settings
#密码加密
from django.contrib.auth.hashers import make_password, check_password
# 全局变量
from nono import globalvariable
# Create your views here.
# 主页
def index(request):
    # login(request)
    if not globalvariable.logined:
        return userLogin(request)


    # userid = request.user.username
    try:
        username=request.session['username']
        userinfo=UserProfile.objects.get(username=username)
    except:
        globalvariable.logined=False
        return  userLogin(request)
        pass
    # topmenu = UserProfile.objects.all()[:1]
    try:

        userinfo1 = Userinfo.objects.get(belong=UserProfile.objects.filter(username=request.session['username'])[0])

        context = {
            'userinfo':userinfo1,
            'authentication': userinfo.status
        }
    except Exception as e:
        context = {
            'userinfo': userinfo,
            'authentication': userinfo.status
        }
        pass
    if username=="admin":
        return index1(request)
    else:
        return render(request, 'eva/Amadeus-index.html', context)

#管理员主页
def index1(request):
    if not globalvariable.logined:
        return userLogin(request)


    # userid = request.user.username
    username=request.session['username']
    userinfo=UserProfile.objects.get(username=username)
    usern={}
    image = {}
    imagepath={}
    path = os.path.join(settings.MEDIA_ROOT, "photo")
    userstatus=UserProfile.objects.all()
    i=0
    for user in userstatus:
        if user.status=='1':
            try:
                usern[user.username]=Personalauthentication.objects.get(belong=UserProfile.objects.filter(username=user.username)[0])
                imagepath[user.username] = os.path.join(path, user.username)
                for files in os.listdir(imagepath[user.username]):
                    id=i+1
                    i=id
                    image[(user.username,id)]= os.path.join(imagepath[user.username], files)
            except Exception as e:
                pass

    try:
        userinfo1 = Userinfo.objects.get(belong=UserProfile.objects.filter(username=request.session['username'])[0])
        context = {
            'userinfo': userinfo1,
            'authentication': userinfo.status,
            'usern':usern,
            'image': image,
        }

    except Exception as e:
        context = {
            'userinfo': userinfo,
            'authentication': userinfo.status,
            'usern': usern,
            'image': image,
        }
        pass
    return render(request,'eva/admin.html',context)

# AI交流
def ai(request):
    # globalvariable.flag=not globalvariable.flag
    globalvariable.flag = True

    if globalvariable.flag:
        # aimain(request,globalvariable.flag)

        try:
            ai_speech(globalvariable.ai_speak)
            play()
            rec()
            speak = listen()
            globalvariable.ai_speak = robot(request, speak)
            if speak == "关闭聊天":
                globalvariable.flag = False
                globalvariable.ai_speak = "来和我聊天吧~"
                return HttpResponse(json.dumps({'speak': "已关闭聊天~", 'flag': globalvariable.flag}))
            return HttpResponse(json.dumps({'speak':globalvariable.ai_speak,'flag':globalvariable.flag}))
        except Exception as e:
            globalvariable.ai_speak="我没听清，再说一遍吧~"
            return HttpResponse(json.dumps({'speak': globalvariable.ai_speak, 'flag': globalvariable.flag}))
            pass
    else:
        return index(request)

# 用户登录
def userLogin(request):
    # if not isinstance(request.user, User):
    #     return redirect(to='aiindex')
    # login(request)
    if request.method=='POST':
        if not globalvariable.logined:
            username=request.POST.get('username')
            password = request.POST.get('password')
            try:
                user=UserProfile.objects.get(username=username)

                if check_password(password, user.password):
                    user.save()
                    # session会话保存,username,token
                    request.session['username'] = username
                    # request.session['password']=password
                    request.session['token'] = user.token

                    # 已登录
                    globalvariable.logined=True
                    if username == "admin":
                        return index(request)
                    return index(request)
                else:
                    context={'info':'密码错误'}
                    print(context)
                    return render(request, 'eva/Amadeus-userlogin.html', context)
            except Exception as e:
                    context = {'info': '该用户名不存在'}
                    print(e)
                    pass
                    return render(request, 'eva/Amadeus-userlogin.html',context)

        elif globalvariable.logined:
            return index(request)
    else:
        if globalvariable.logined:
            return index(request)
        else:
            return render(request, 'eva/Amadeus-userlogin.html')
def userLogin1(request):
    return render(request, 'eva/Amadeus-userlogin1.html')
#用户登出
def userlogout(request):
    logout(request)
    globalvariable.logined=False
    return redirect('/')

# 用户注册
def userregistration(request):
    # if not isinstance(request.user, User):
    #     return redirect(to='aiindex')
    # else:
    if request.method=='POST':
        # print(request.method)
        username=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        status=0
        try:
            user=Userinfo.objects.filter(username=username).all()
            if not (user.count()==0):
                context={'info':"用户名已被使用"}
                return render(request, 'eva/Amadeus-userregistration.html', context)
        except Exception as e:
            pass

        if password==password1 and len(password)>=6:

            #制作tokem
            token=time.time()+random.randrange(1,1000000)
            token=str(token)
            # 密码加密
            password=make_password(password)
            user=UserProfile.createuser(username,email,password,token,status)
            user.save()
            #session会话保存,username,token
            request.session['username']=username
            request.session['token']=token
            return redirect('/')
        elif len(password)<6:
            context = {'info': '密码长度至少为6位'}
        elif password!=password1:
            context = {'info': '密码与确认密码不符合'}
        return render(request, 'eva/Amadeus-userregistration.html',context)
    else:
        # print(request.method)
        return render(request, 'eva/Amadeus-userregistration.html')

# 个人信息
def personalinformation(request):
    if not globalvariable.logined:
        return userLogin(request)

    if request.method=='POST':

        nickname=request.POST.get('nickname')
        autograph = request.POST.get('autograph')
        occupation = request.POST.get('occupation')
        company = request.POST.get('company')
        phonenumber = request.POST.get('phonenumber')


        sex = request.POST.get('sex')
        Birthday = request.POST.get('Birthday')
        headportrait = request.FILES.get('headportrait')
        personalstatement = request.POST.get('personalstatement')
        belong=UserProfile.objects.filter(username=request.session['username'])[0]
        headportrait=upload_path(request,headportrait,"headportrait")

        try:
            user=Userinfo.objects.filter(belong=belong).all()
            # 已填写个人信息
            if (user.count() == 0):
                globalvariable.personalinformation = False
            else:
                globalvariable.personalinformation = True
            # print(user)
        except Exception as e:
            print(e)

            pass
        context={}
        # if len(str(phonenumber)):
        #     if re.findall('^1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}$', phonenumber):
        #         print("是正确的手机号")
        #
        #     else:
        #         context = {'info_phonenumber': '手机号不正确，请重新输入'}

        try:
            print(globalvariable.personalinformation)
            if globalvariable.personalinformation:
                user = Userinfo.objects.filter(belong=belong).update(nickname=nickname, autograph=autograph, occupation=occupation, company=company,
                                       phonenumber=phonenumber, sex=sex, Birthday=Birthday, headportrait=headportrait,
                                       personalstatement=personalstatement, belong=belong)


            else:
                user = Userinfo.objects.create(nickname=nickname, autograph=autograph, occupation=occupation,
                                               company=company, phonenumber=phonenumber, sex=sex, Birthday=Birthday,
                                               headportrait=headportrait, personalstatement=personalstatement, belong=belong)
                user.save()
        except Exception as e:
            print(e)
            pass
        # for i in range(len(user)):
        #     user[i].save()


        return redirect('/eva')
    else:
        username = request.session['username']
        userinfo=UserProfile.objects.get(username=username)
        try:
            userinfo1 = Userinfo.objects.get(belong=UserProfile.objects.filter(username=request.session['username'])[0])
            context = {
                'userinfo': userinfo1,
                'authentication': userinfo.status
            }
        except Exception as e:
            userinfo = UserProfile.objects.get(username=request.session['username'])
            pass
            context = {
                'userinfo': userinfo,
                'authentication': userinfo.status
            }

        return render(request,'eva/personalinformation.html',context)
# 实名认证
def authentication(request):
    if not globalvariable.logined:
        return userLogin(request)

    if request.method=='POST':

        name=request.POST.get('name')
        idnumber = request.POST.get('idnumber')
        idfrontphoto = request.FILES.get('idfrontphoto')
        idbackphoto = request.FILES.get('idbackphoto')

        photo31 = request.FILES.get('photo31')
        photo32 = request.FILES.get('photo32')
        photo33 = request.FILES.get('photo33')
        photo34 = request.FILES.get('photo34')
        photo35 = request.FILES.get('photo35')
        # print(photo31)

        belong=UserProfile.objects.filter(username=request.session['username'])[0]
        idfrontphoto=upload_path(request, idfrontphoto, "idphoto")
        idbackphoto = upload_path(request, idbackphoto, "idphoto")
        photo31 = upload_path(request, photo31, "photo")
        photo32 = upload_path(request, photo32, "photo")
        photo33 = upload_path(request, photo33, "photo")
        photo34 = upload_path(request, photo34, "photo")
        photo35 = upload_path(request, photo35, "photo")
        try:
            user=Personalauthentication.objects.filter(belong=belong).all()
            # 已实名认证
            if(user.count()==0):
                status=0
            else:
                status = 1
            print(user.count())
        except Exception as e:
            print(e)
            status=0
            pass

        try:

            if status:
                user = Personalauthentication.objects.filter(belong=belong).update(name=name, idnumber=idnumber, idfrontphoto=idfrontphoto,
                                       idbackphoto=idbackphoto,photo1=photo31,photo2=photo32,photo3=photo33,photo4=photo34,photo5=photo35,belong=belong)

                UserProfile.objects.update(status=status)
            else:
                user = Personalauthentication.objects.create(name=name, idnumber=idnumber,
                                                                     idfrontphoto=idfrontphoto,
                                                                     idbackphoto=idbackphoto, photo1=photo31,
                                                                     photo2=photo32, photo3=photo33, photo4=photo34,
                                                                     photo5=photo35, belong=belong)
                user.save()
                UserProfile.objects.update(status=status)
        except Exception as e:
            print(e)
            pass

        return redirect('/eva')
    else:

        try:
            username=request.session['username']
            user=UserProfile.objects.get(username=username)
            userinfo1 = Userinfo.objects.get(belong=UserProfile.objects.filter(username=request.session['username'])[0])
            context = {
                'userinfo': userinfo1,
                'authentication': user.status,
            }
        except Exception as e:
            userinfo = UserProfile.objects.get(username=request.session['username'])
            pass
            context = {
                'userinfo': userinfo,
            }
        # print(UserProfile.objects.filter(username=request.session['username'])[0])
        return render(request,'eva/Amadeus-authentication.html',context)



# 404
def page404(request):
    return render(request, 'eva/404.html')

# 上传文件
def upload_path(request,photo,filename):
    try:
        username=request.session["username"]
        ext=photo.name.split('.')[-1]
        if ext.lower() in ["jpg","jpeg", "png", "gif"]:
            sub_folder = filename
        if ext.lower() in ["pdf", "docx","txt"]:
            sub_folder = "other"
        save_path=os.path.join(settings.MEDIA_ROOT, sub_folder, username)
        print(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        photo_path=os.path.join(save_path,photo.name)
        with open(photo_path,'wb')as f:
            for content in photo.chunks():
                f.write(content)
        if photo_path is None:
            photo_path=''
        return photo_path
    except Exception as e:
        pass
# 判断是否登录
def login(request):
    try:
        username = request.session["username"]
        password = request.session["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            globalvariable.logined=True
        else:
            globalvariable.logined=False
    except Exception as e:
        pass
    return globalvariable.logined

def charts(request):
    if not globalvariable.logined:
        return userLogin(request)
    username = request.session['username']
    userinfo = UserProfile.objects.get(username=username)
    try:
        userinfo1 = Userinfo.objects.get(belong=UserProfile.objects.filter(username=request.session['username'])[0])
        context = {
            'userinfo': userinfo1,
            'authentication': userinfo.status
        }
    except Exception as e:
        context = {
            'userinfo': userinfo,
            'authentication': userinfo.status
        }
        pass
    return render(request, 'eva/charts/charts-chartjs.html',context)
def reptile(request):
    name=request.GET.get('content')
    # page=request.GET.get('page1')
    # print(page)
    remain(name,10)
    return HttpResponse("ok")
def a(request):
    return render(request, 'eva/charts/Regional_distribution_bar.html')
def b(request):
    return render(request, 'eva/charts/Regional_distribution_geo.html')
def c(request):
    return render(request, 'eva/charts/学历情况.html')
def d(request):
    return render(request, 'eva/charts/工作经验.html')
def e(request):
    return render(request, 'eva/charts/薪资待遇.html')