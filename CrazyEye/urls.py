"""CrazyEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name='index'),
    re_path('^$',views.index,name='index'),
    path('test/',views.test,name='test'),
    path('login/',views.acc_login,name='login'),
    path('logout/',views.acc_logout,name='logout'),
    path('hosts/',views.display_hosts,name='display_hosts'),
    path('hosts/<int:current_page>/',views.display_hosts),
    path('connect_host/<int:bind_host_id>',views.connect_host,name='connect_host'),
    path('audit/',views.audit),
]
