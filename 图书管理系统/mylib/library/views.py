from django.shortcuts import render,HttpResponse,redirect
from library.models import libdata      # 自定义的数据类
# Create your views here.

import json
def book(request):
    # if request.method == 'GET':
    data = libdata.objects.all()
    return render(request,'book.html',{'data':data})

def add(request):
    if request.method == 'GET':
        return render(request,'add.html')
    else:
        price = request.POST.get('price')
        title = request.POST.get('title')
        athor = request.POST.get('athor')
        pub_date = request.POST.get('pub_date')
        publish = request.POST.get('publish')
        libdata.objects.create(price=price,title=title,athor=athor,pub_date=pub_date,publish=publish)
        return redirect('/book')

# 修改视图函数
def update(request,id):
    bookdata = libdata.objects.filter(id=id).first()
    if request.method == 'GET':
        return render(request,'update.html',{'bookdata':bookdata})
    else:
        price = request.POST.get('price')
        title = request.POST.get('title')
        athor = request.POST.get('athor')
        pub_date = request.POST.get('pub_date')
        publish = request.POST.get('publish')
        libdata.objects.filter(id=id).update(price=price,title=title,athor=athor,pub_date=pub_date,publish=publish)
        return redirect('/book')

# 删除视图函数
def delete(request,id):
    libdata.objects.filter(id=id).delete()
    return redirect('/book')

# 作者详情页
def athor(request,athor):
    athordata = libdata.objects.filter(athor=athor)
    # athordata = libdata.objects.filter(athor=athor).values('athor','title')
    # print(athordata)
    return render(request,'athor.html',{'athordata':athordata,'athor':athor})

# 出版社详情页
def publish(request,publish):
    publishdata = libdata.objects.filter(publish=publish)
    # print(publishdata)
    return render(request,'publish.html',{'publishdata':publishdata,'publish':publish})