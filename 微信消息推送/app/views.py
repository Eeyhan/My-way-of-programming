from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
import requests
from app import models
import json


# Create your views here.
def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    # models.UserInfo.objects.create(username='luffy',password=123)

    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            request.session['user_info'] = {'id': obj.id, 'name': obj.username, 'uid': obj.uid}
            return redirect('/bind/')
    else:
        return render(request, 'login.html')


def bind(request):
    """用户绑定页面"""
    return render(request, 'auth.html')


def bindQrcode(request):
    """生成二维码"""
    ret = {'code': 1000}
    try:
        access_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}#wechat_redirect"
        access_url = access_url.format(
            appid=settings.WECHAT_CONFIG["app_id"],
            redirect_uri=settings.WECHAT_CONFIG["redirect_uri"],
            state=request.session['user_info']['uid']
        )
        ret['data'] = access_url
    except Exception as e:
        ret['code'] = 1001
        ret['msg'] = str(e)
    return JsonResponse(ret)


def callback(request):
    """
    用户在手机微信上扫码后，微信自动调用该方法。
    用于获取扫码用户的唯一ID，以后用于给他推送消息。
    :param request:
    :return:
    """
    code = request.GET.get("code")

    # 用户UID
    state = request.GET.get("state")

    # 获取该用户openId(用户唯一，用于给用户发送消息)
    res = requests.get(
        url="https://api.weixin.qq.com/sns/oauth2/access_token",
        params={
            "appid": settings.WECHAT_CONFIG["app_id"],
            "secret": settings.WECHAT_CONFIG["appsecret"],
            "code": code,
            "grant_type": 'authorization_code',
        }
    ).json()
    # 获取的到openid表示用户授权成功

    openid = res.get("openid")
    if openid:
        models.UserInfo.objects.filter(uid=state).update(wx_id=openid)
        response = "<h1>授权成功 %s </h1>" % openid
    else:
        response = "<h1>用户扫码之后，手机上的提示</h1>"
    return HttpResponse(response)


def get_access_token():
    """获取token"""
    result = requests.get(
        url='https://api.weixin.qq.com/cgi-bin/token',
        params={
            "grant_type": "client_credential",
            "appid": settings.WECHAT_CONFIG['app_id'],
            "secret": settings.WECHAT_CONFIG['appsecret'],
        }
    ).json()
    if result.get('access_token'):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token


def send_content_msg(user_id, access_token):
    """内容消息发送"""
    body = {
        'touser': user_id,
        'msgtype': 'text',
        'text': {
            'content': '内容。。。。。不是模板消息'
        }
    }
    response = requests.post(
        url='https://api.weixin.qq.com/cgi-bin/message/custom/send',
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    result = response.json()
    return result


def send_template_msg(user_id, access_token):
    """模板消息发送"""
    result = requests.post(
        url='https://api.weixin.qq.com/cgi-bin/message/template/send',
        params={
            'access_token': access_token
        },
        json={
            "touser": user_id,
            "template_id": settings.WECHAT_CONFIG['template_id'],
            "data": {
                "first": {
                    "value": "微信模板页面发送消息",
                    "color": "#173177"
                },
                "kw1": {
                    "value": "卧槽调这个参数搞了有点久",
                    "color":"#173177"
                },
                "kw2": {
                    "value": "可不是咋地"
                },
                "kw3": {
                    "value": "就看这次能不能成功了"
                },
            }
        }
    )
    result = result.json()
    return result


def sendmsg(requet):
    access_token = get_access_token()
    # 这里由于我本来就只有一个数据，所以直接写死了，真实的开发当然是用当前登录用户扫码关注的用户对应
    userobj = models.UserInfo.objects.filter(id=1).first()
    # 发送模板消息
    result = send_template_msg(userobj.wx_id, access_token)

    # 发送正文消息
    # result = send_content_msg(userobj.wx_id, access_token)

    if result.get('errcode') == 0:
        return HttpResponse('发送成功')
    return HttpResponse('发送失败')
