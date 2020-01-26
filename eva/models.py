from django.db import models
from django.contrib.auth.models import User

# Create your models here.



#用户注册
class UserProfile(models.Model):
    username=models.CharField(max_length=20,verbose_name=u'用户名',unique=True)
    email=models.EmailField(max_length=64,blank=True,null=True,verbose_name=u'邮箱')
    password=models.CharField(max_length=100,verbose_name=u'密码')
    icon=models.ImageField(blank=True,null=True,max_length=200)
    created=models.DateTimeField(auto_now_add=True,verbose_name="用户注册时间")
    updated=models.DateTimeField(auto_now=True,verbose_name="用户更新时间")
    token=models.CharField(max_length=256,verbose_name=u'Token')
    # 0: 未认证 1:等待认证 2：已认证
    status = models.CharField(max_length=20,null=True, blank=True,verbose_name=u'认证状态')
    @classmethod
    def createuser(cls,username,email,password,token,status):
        u=cls(username=username,email=email,password=password,token=token,status=status)
        return u
    def __str__(self):
        return self.username
# 用户拓展资料
class Userinfo(models.Model):
    nickname = models.CharField(max_length=20,verbose_name=u'昵称')
    autograph = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'签名')
    occupation=models.CharField(max_length=20,blank=True,null=True,verbose_name=u'职业')
    company = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'公司')
    phonenumber = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'手机号')
    sex = models.CharField(max_length=2, blank=True, null=True, verbose_name=u'性别')
    Birthday = models.DateField( blank=True, null=True, verbose_name=u'生日')
    headportrait = models.ImageField(null=True, blank=True,verbose_name=u'头像')
    personalstatement = models.TextField(max_length=400, blank=True, null=True, verbose_name=u'个人说明')

    belong = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True,related_name='nikename')

    @classmethod
    def createuser1(cls, nickname, autograph, occupation, company,phonenumber,sex,Birthday,headportrait,Personalstatement):
        u = cls(nickname=nickname, autograph=autograph, occupation=occupation, company=company,phonenumber=phonenumber,sex=sex,Birthday=Birthday,headportrait=headportrait,Personalstatement=Personalstatement)
        return u
    def __str__(self):
        return self.nickname

# 个人实名认证
class Personalauthentication(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'姓名')
    idnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'身份证号')
    idfrontphoto = models.ImageField(null=True, blank=True, verbose_name=u'身份证正面照')
    idbackphoto = models.ImageField(null=True, blank=True, verbose_name=u'身份证背面照')
    photo1 = models.ImageField(null=True, blank=True, verbose_name=u'照片1')
    photo2 = models.ImageField(null=True, blank=True, verbose_name=u'照片2')
    photo3 = models.ImageField(null=True, blank=True, verbose_name=u'照片3')
    photo4 = models.ImageField(null=True, blank=True, verbose_name=u'照片4')
    photo5 = models.ImageField(null=True, blank=True,verbose_name=u'照片5')

    belong = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True,related_name='name')

    @classmethod
    def createuser1(cls, name, idnumber, idfrontphoto, photo1,photo2,photo3,photo4,photo5):
        u = cls(name=name, idnumber=idnumber, idfrontphoto=idfrontphoto, photo1=photo1,photo2=photo2,photo3=photo3,photo4=photo4,photo5=photo5)
        return u
    def __str__(self):
        return self.name