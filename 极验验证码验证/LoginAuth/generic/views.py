from django.shortcuts import render
from rest_framework.views import APIView
import redis
from utils.geetest import GeetestLib
from django.http import HttpResponse
import json

# Create your views here.

pc_geetest_id = "64936e8e1ad53dad8bbee6f96224e7d0"
pc_geetest_key = "8322ed330d370a704a77d8205c94d20f"
CONN = redis.Redis(host='127.0.0.1')  # 前提自己安装上redis并配置好可以连接

class AuthView(APIView):
    def get(self, request):
        return render(request, "index.html")


class GtView(APIView):
    def get(self, request):
        user_id = 'test'
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = gt.pre_process(user_id)
        # request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id
        CONN.set(gt.GT_STATUS_SESSION_KEY, status)
        CONN.set("user_id", user_id)
        response_str = gt.get_response_str()
        return HttpResponse(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        status = CONN.get(gt.GT_STATUS_SESSION_KEY)
        user_id = CONN.get("user_id")
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return HttpResponse(json.dumps(result))
