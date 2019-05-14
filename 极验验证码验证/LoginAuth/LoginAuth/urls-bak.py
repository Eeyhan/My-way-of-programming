"""LoginAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from generic.views import AuthView
# from generic.views import GtView

from django.contrib import admin
from django.urls import re_path, path
from generic.views import login, get_valid_code_img

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('get_validCode_img/', get_valid_code_img),

    # re_path(r'^pc-geetest/register', GtView.as_view()),
    # re_path(r'^pc-geetest/validate$', GtView.as_view()),
    # path('auth/', AuthView.as_view()),
]
