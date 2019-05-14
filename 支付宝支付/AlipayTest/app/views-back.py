from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.domain.AlipayTradePrecreateModel import AlipayTradePrecreateModel
from alipay.aop.api.request.AlipayTradePrecreateRequest import AlipayTradePrecreateRequest
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
import time

# Create your views here.
# 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
# "https://openapi.alipaydev.com/gateway.do", APP_ID, APP_PRIVATE_KEY, "json", CHARSET, ALIPAY_PUBLIC_KEY, "RSA2"


def Ali_pay():
    # 为阿里支付实例化一个配置信息对象
    alipay_config = AlipayClientConfig(sandbox_debug=True)
    # 初始化各种配置信息
    # 阿里提供服务的接口
    alipay_config.server_url = "https://openapi.alipaydev.com/gateway.do"
    # 申请的沙箱环境的app_id
    alipay_config.app_id = "2016092700611690"
    # 商户的私钥
    with open("keys/private_key.txt") as f:
        alipay_config.app_private_key = f.read()
    # 阿里的公钥
    with open("keys/public_key.txt") as f:
        alipay_config.alipay_public_key = f.read()
    # 实例化一个支付对象并返回
    alipay_client = DefaultAlipayClient(alipay_client_config=alipay_config)
    return alipay_client


class AlipayView(APIView):
    def get(self, request):
        return render(request, 'pay.html')

    # 生成支付宝自带页面的API
    def post(self, request):
        money = request.data.get('money')
        if not money.isdigit():
            return Response('错误，只能是数字')
        money = int(money)

        # 得到阿里支付的实例化对象
        client = Ali_pay()
        # 为API生成一个模板对象 初始化参数用的
        model = AlipayTradePagePayModel()
        # 订单号
        model.out_trade_no = "pay" + str(time.time())
        # 金额
        model.total_amount = money
        # 商品标题
        model.subject = "测试"
        # 商品详细内容
        model.body = "支付宝测试"
        # 销售产品码，与支付宝签约的产品码名称
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        # 实例化一个请求对象
        request = AlipayTradePagePayRequest(biz_model=model)
        # get请求 用户支付成功后返回的页面请求地址
        request.return_url = "http://140.143.63.45:8888/alipay_handler"
        # post请求 用户支付成功通知商户的请求地址
        request.notify_url = "http://140.143.63.45:8888/alipay_handler"
        # 利用阿里支付对象发一个获得页面的请求 参数是request
        response = client.page_execute(request, http_method="GET")
        return redirect(response)


class PayHandlerView(APIView):
    def get(self, request):
        # return_url的回调地址
        print(request.data)
        # 用户支付成功之后回到哪
        return HttpResponse("return_url测试")

    def post(self, request):
        print(request.data)
        # 用户支付成功 在这里修改订单状态以及优惠券贝里等等情况
        return HttpResponse("notify_url")
