# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from utils.geetest import GeetestLib

pc_geetest_id = "64936e8e1ad53dad8bbee6f96224e7d0"
pc_geetest_key = "8322ed330d370a704a77d8205c94d20f"


class AuthView(View):
    def get(self, request):
        return render(request, "index.html")


class GtView(View):
    def get(self, request):
        user_id = 'test'
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = gt.pre_process(user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        return HttpResponse(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
        return HttpResponse(result)
