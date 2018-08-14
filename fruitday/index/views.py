from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
import json
from django.core import serializers
# Create your views here.


# def login_views(request):
#     return render(request,'01_login.html')



# def login_views(request):
    # if request.method == 'GET':
    #     #判断cookies中是否包含登录信息
    #     if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
    #         return HttpResponse('欢迎:' + request.COOKIES['uphone']　)
    #     #创建LoginForm对象,再交给模板
    #     else:
    #         form = LoginForm()
    #         return render(request, 'login.html',locals())
    # else:
    #     uphone = request.POST['uphone']
    #     upwd = request.POST['upwd']
    #     uList = Users.objects.filter(uphone=uphone, upwd=upwd)
    #     if uList:
    #         resp = HttpResponse('欢迎:' + uphone)
    #         if 'isSaved' in request.POST:
    #             # 
    #             expires = 60*60*24*365
    #             resp.set_cookie('id',uList[0].id, expires)
    #             resp.set_cookie('uphone',uphone,expires)

        
    #         return resp
    #     else:
    #         form = LoginForm()
    #         return render(request, 'login.html',locals())









def register_views(request):
    if request.method == 'GET':

        return render(request,'register.html')
    else:
        # 接收提交的数据并注册回数据库
        uphone = request.POST['uphone']
        #验证手机号码是否已经存在
        
        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        Ulist = Users.objects.filter(uphone=uphone)
        
        if Ulist:
            return render(request,'register.html',
                    {'<errMsg':'手机号已经存在',
                    'uname':uname,
                    'uemail':uemail,
                })


        dict = {
            'uphone': uphone,
            'upwd': upwd,
            'uname': uname,
            'uemail': uemail,

        }

        Users(**dict).save()
        return HttpResponse('注册成功')

def login_views(request):
    if request.method == 'POST':
        # 处理post请求
        # 实现登录操作
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uList = Users.objects.filter(uphone=uphone, upwd=upwd)
        # 判断登录成功or 失败
        if uList:
            #从cookie中获取登录页面之前的url
            url =request.COOKIES.get('url')
            resp = HttpResponseRedirect(url)
            #从cookie中将url删除
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            expires = 60 * 60 * 24 * 365

            # 登录成功
            # 将登录信息保存进session
            request.session['uphone'] = uphone
            request.session['id'] = uList[0].id
            # 是否记住密码
            if 'isSaved' in request.POST:
                # 将登录信息保存进cookie
                resp.set_cookie('id', uList[0].id, expires)
                resp.set_cookie('uphone', uphone, expires)
            return resp


        else:
            #  登录失败
            # 继续展示登录页面
            form = LoginForm()
            return render(request, 'login.html', locals())



    else:
        # 处理get请求
        #获取原地址(请求此处的地址)
        url = request.META.get('HTTP_REFERER','/')
        #通过url构建响应对象
        resp = HttpResponseRedirect(url)
        # 判断session中是否有id 和uphone
        if 'id' in request.session and 'uphone' in request.session:
            # session中有登录信息，直接区首页
            return resp
        else:
            # session中没有登录信息
            if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
                #　曾经登录过，而且保存了信息，取出数据保存进session
                uid = request.COOKIES['id']
                uphone = request.COOKIES['uphone']
                request.session['id'] = uid
                request.session['uphone'] = uphone
                return resp
            else:
                #cookies中也没有登录信息
                form =LoginForm()
                #将url保存进cookie
                resp = render(request, 'login.html', locals())
                resp.set_cookie('url',url)
                return resp



def checkphone_views(request):
    #1.接收前端提交过来的数据-uphone
    uphone=request.GET['uphone']
    #2.查询uphone在数据表中是否存在
    u_list = Users.objects.filter(uphone=uphone)
    #3.如果存在响应：{"status":1}如果不存在响应:{"status":0}
    if u_list:
        s=1
        msg = '用户已存在'
    else:
        s=0
        msg = '通过'
    dic = {"status":s,'msg':msg}
    return HttpResponse(json.dumps(dic))

def index_views(request):
    list_type = GoodsType.objects.all()

    return render(request,'index.html',locals())


def all_type_goods_views(request):
    #大列表盛装所有的类型和商品
    all_list = []
    #查询所有类型
    types = GoodsType.objects.all()
    #循环遍历types，得到每一个type以及对应的商品们
    for type in types:
        # 将type序列化为json字符串
        type_json = json.dumps(type.to_dict())
        # print(type_json)
        # 获取type下的5个产品
        g_list = type.goods_set.order_by("-id")[0:5]
        # 将g_list序列化成json的字符串
        g_list_json = serializers.serialize('json',g_list)
        # print(g_list_json)
        # 创建一个字典，将type_json和g_list_json封装
        dic = {
            "type":type_json,
            "goods":g_list_json,
        }
        # 将字典追加进all_list列表中
        all_list.append(dic)

    return HttpResponse(json.dumps(all_list))



#验证用户是否处于登录状态
def check_login_views(request):
    #验证session中是否包含登录信息
    if 'id' in request.session and 'uphone' in request.session:
        #已经处于登录状态
        loginStatus = 1
        #通过session中的id获取uname
        id=request.session.get('id')
        uname = Users.objects.get(id=id).uname
        dic = {
            "loginStatus":loginStatus,
            "uname":uname

        }
        return HttpResponse(json.dumps(dic))
    else:
        #session中没有登录信息
        #查询COOKIES中是否包含登录信息
        if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
            user_id = request.COOKIES['id']
            uphone = request.COOKIES['uphone']
            #将user_id和uphone保存进session
            request.session['id'] = user_id
            request.session['uphone'] = uphone
            #查询uname的值响应给客户端
            uname = Users.objects.get(id=user_id).name
            loginStatus = 1
            dic = {
                "loginStatus":loginStatus,
                "uname":uname

            }
            return HttpResponse(json.dumps(dic))
        else:
            #session和cookies中均没有登录信息
            dic = {
                "loginStatus":0
            }
            return HttpResponse(json.dumps(dic))


def logout_views(request):
    if 'id' in request.session and 'uphone' in request.session:
        #将id 和session的值从session中移出去
        del request.session['id']
        del request.session['uphone']
        #记录源地址
        url = request.META.get('HTTP_REFERER','/')
        resp =HttpResponseRedirect(url)
        #判断cookie中是否包含登录信息，再决定是否删除
        if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('id')
            resp.delete_cookie('uphone')
        return resp
    return HttpResponseRedirect('/')

#添加或更新购物车的内容
def add_cart_views(request):
    #接收数据
    user_id = request.session.get('id')
    good_id = request.POST['good_id']
    good_count = 1
    #查看购物车中是否有相同产品，如果有的话更新数量即可，否则新增数据
    cart_list = CartInfo.objects.filter(user_id=user_id,good_id=good_id)
    if cart_list:
        #已经有商品了，更新数量即可
        cartinfo=cart_list[0]
        cartinfo.count = cartinfo.ccount+good_count
        cartinfo_save()
        dic = {
            'status':1,
            'statusText':'更新数量成功'

        }
        return HttpResponseRedirect(json.dumps(dic))
    else:
        #没有商品，需插入数据到数据库中
        cartinfo = CartInfo()
        cartinfo.good_id = good_id
        cartinfo_user_id = user_id
        cartinfo.ccount = good_count
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'添加购物车成功'
        }
        return HttpResponse(json.dumps(dic))


def dict_views(request):
    return render(request,'01_dict.html')







