import json
import xlrd
import pandas as pd
from scipy import stats
import numpy as np

from tools import vis, abtest, did, misc, matching, ml #, ttest, did
from django.shortcuts import render, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
'''def ful(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
             username = uf.cleaned_data['username']
             headImg = uf.cleaned_data['headImg']
             file = file_uploaded ()
             file.username = username
             file.headImg = headImg
             file.save()
             return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render(request,'register.html',{'uf':uf})
'''


def file_upload(request):
    if request.method == "POST":
        file = request.FILES.getlist('file')[0]
        url = './upload/' + file.name
        global path
        path = url
        print(path)
        with open(url, 'wb')as f:
            for data in file.chunks():
                f.write(data)
        return HttpResponse(file)


def vis_exp(request):
    if request.method == "GET":
        index, data = vis.vis(path)
        content = {
            'index': index,
            'data': data
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def abtest_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)

        digit = data.get('digit')
        binomial = data.get('chi_squared_columns')
        conf = data.get('conf')
        segment = data.get('segment')

        file_dl = abtest.ab_test(path, digit, binomial, conf)
        file = open(file_dl, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="test.xlsx" '
        return response


def did_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)

        treatment_col = data.get('treatment_col')
        id_col = data.get('id_col')
        date_col = data.get('date_col')
        y = data.get('dv')
        post = data.get('date')

        res, p, coef = did.did(path, treatment_col, id_col, date_col, y, post)
        content = {
            'res': res,
            'p_value': p,
            'coef': coef
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def ttest_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mode = data.get('mode')
        conf = data.get('conf')
        y = data.get('y')
        res, p = misc.t_test(path, conf, mode, y)
        content = {
            'res': res,
            'p_value': p
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def chitest_exp(request):
    if request.method == "GET":
        res, p = misc.chi_test(path)
        content = {
            'res': res,
            'p_value': p
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def lt_pred_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        days= data.get('days')
        mse, x, y, y_pred = misc.lt_pred(path, days)
        content = {
            'mse': mse,
            'x': x,
            'y': y,
            'y_pred': y_pred
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def cem_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        feature_col_first = data.get('first_feature')
        feature_col_last = data.get('last_feature')
        matching.CEM(path,feature_col_first,feature_col_last)
        return HttpResponse()


def psm_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        features = data.get('features')
        model = data.get('model')
        label = data.get('label')
        caliper = data.get('caliper')
        top = data.get('top')
        matched, pscore, match_id, feature_importance = matching.PSM(path, features, model, label, caliper, top)
        content = {
            'matched': matched,
            'p_value': p
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def ml_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)

        ml_type = data.get('ml_type')
        if ml_type == 'clu':
            model = data.get('model')
            cluster = data.get('cluster')
            file_dl = ml.cluster(path, model, cluster)
        elif ml_type == 'cla':
            model = data.get('model')
            length = data.get('length')
            kernel = data.get('kernel')
            neighbors = data.get('neighbors')
            file_dl = ml.classify(path, model, length, kernel, neighbors)

        file = open(file_dl, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="test.xlsx" '
        return response


def test(request):
    if request.method == "GET":
        res ='test-test-test'
        return HttpResponse(res)


def file_download(request):
    if request.method == "POST":
        data = json.loads(request.body)
        flag = data.get('test')
        file=''
        if flag=='1':
            file = open('./upload/test.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  #设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="test.xlsx" '
        print('ok')
        return response

