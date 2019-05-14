# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont
import random
import io


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_valid_code_img(request):
    # 方式1 :
    img = Image.new("RGB", (270, 40), color=get_random_color())
    draw = ImageDraw.Draw(img)
    arial_font = ImageFont.truetype("arial.ttf", size=26)
    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 30 + 30, 0), random_char, get_random_color(), font=arial_font)
        # 保存验证码字符串
        valid_code_str += random_char
    width = 170
    height = 30
    # 噪线
    for i in range(3):  # 三条线，也可以更多
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 噪点
    for i in range(50): # 50个噪点，也可以更多
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 登录验证相关
    request.session["valid_code_str"] = valid_code_str
    request.session['count'] = 0
    # with open("validCode.png", "wb") as f:
    #     img.save(f, "png")
    # with open("validCode.png", "rb") as f:
    #     data = f.read()
    f = io.BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return HttpResponse(data)


def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        valid_code_str = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # request.user== 当前登录对象
                response["user"] = user.username
            else:
                response["msg"] = "用户名或者密码错误!"
        else:
            response["msg"] = "验证码错误!"
        return JsonResponse(response)
    return render(request, "login.html")
