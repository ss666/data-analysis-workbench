"""sp_v0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from back_end.views import file_upload,vis_exp,abtest_exp,did_exp,ttest_exp,chitest_exp,lt_pred_exp,cem_exp,psm_exp,ml_exp,test,file_download
urlpatterns = [
    path('admin/', admin.site.urls),
    path('file_upload/', file_upload),
    path('vis/',vis_exp),
    path('abtest/', abtest_exp),
    path('did/', did_exp),
    path('ttest/', ttest_exp),
    path('chitest/', chitest_exp),
    path('lt/', lt_pred_exp),
    path('cem/', cem_exp),
    path('psm/', psm_exp),
    path('ml/', ml_exp),
    path('test/', test),
    path('download/', file_download),  #有没有 ,
]
