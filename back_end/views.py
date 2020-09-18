import json
import pandas as pd
import xlrd
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
        digit = int(data.get('digit'))
        binomial = data.get('chi_squared_columns')
        conf = float(data.get('conf'))
        #segment = data.get('segment')

        file_name = abtest.ab_test(path, digit, binomial, conf)
        '''
        file_name = 'abtest_result.csv'
        df.to_csv(file_name, index=False)
        # print(file_name)
        with open(file_name, 'rb') as file:
            response = HttpResponse(file)
            response['Content-Type'] = 'text/csv'  # Content-Type header: used to indicate the media type of the resource
            response['Content-Disposition'] = 'attachment;filename="abtest_result.csv"'#"abtest_result.csv" '
        #file = open(file_dl, 'rb')
        #response = HttpResponse(content_type='text/csv')
        #response['Content-Type'] = #'application/octet-stream'
        #response['Content-Disposition'] = 'attachment;filename=abtest_result.csv'
       # df.to_csv(response, index=False)
            print('ok')
        '''
        return HttpResponse(file_name, content_type='application/json')


def did_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)

        treatment_col = data.get('treatment_col')
        id_col = data.get('id_col')
        date_col = data.get('date_col')
        y = data.get('dv')
        post = data.get('date')
        if treatment_col =='':
            treatment_col = 'treatment'
        if id_col == '':
            id_col = 'treatment'

        res, p, effect = did.did(path, y, post, treatment_col, id_col, date_col)
        content = {
            'res': res,
            'p_value': p,
            'effect': effect
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def ttest_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mode = int(data.get('mode'))
        conf = float(data.get('conf'))
        y = float(data.get('y'))
        res, p = misc.t_test(path, conf, mode, y)
        content = {
            'res': res,
            'p_value': p
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def chitest_exp(request):
    if request.method == "GET":
        data = json.loads(request.body)
        alpha = data.get('alpha')
        res, p = misc.chi_test(path, alpha)
        content = {
            'res': res,
            'p_value': p
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def lt_pred_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        arup = int(data.get('arup'))
        days = int(data.get('days'))
        pred_days = int(data.get('pred_days'))
        x, y, y_pred, ltv, base_cnt = misc.lt_pred(path, arup, days, pred_days)
        content = {
            #'mse': mse,
            'x': x,
            'y': y,
            'y_pred': y_pred,
            'ltv': ltv,
            'pred_days': pred_days,
            'base_cnt': int(base_cnt)
        }
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')


def cem_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        feature_col_first = data.get('first_feature')
        feature_col_last = data.get('last_feature')
        matched = matching.cem(path, feature_col_first, feature_col_last)

        file = open(matched, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="cem_matched_dataset.xlsx" '
        return response


def psm_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        treatment_col = data.get('treatment_col')
        id_col = data.get('id_col')
        features = data.get('features').split(':')
        model = data.get('model')
        label = data.get('label')
        caliper = data.get('caliper')
        if caliper == '':
            caliper = 0.5
        else:
            caliper = float(caliper)
        #top = data.get('top')
        feature_col_first = int(features[0]) - 1
        feature_col_last = int(features[1]) - 1
        matched_file_name = matching.psm(path, feature_col_first, feature_col_last,  label, model, caliper, treatment_col, id_col)

        return HttpResponse(matched_file_name, content_type='application/json')


def ml_exp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        file_dl = ''
        print(data)
        print(data.get('ml_type'))

        ml_type = data.get('ml_type')
        if ml_type == 'clu':
            model = data.get('model')
            cluster = data.get('cluster')
            file_dl = ml.cluster(path, model, cluster)
        elif ml_type == 'cla':
            model = data.get('model')
            length = int(data.get('length'))
            kernel = data.get('kernel')
            neighbors = int(data.get('neighbors'))
            file_dl = ml.classify(path, model, length, kernel, neighbors)

        file = open(file_dl, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="test2.xlsx" '
        return response


def test(request):
    if request.method == "GET":
        res ='test-test-test'
        return HttpResponse(res)


def test_file_download(request):
    if request.method == "POST":
        data = json.loads(request.body)
        flag = data.get('test')
        file=''
        if flag=='1':
            file = open('./upload/test.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="test.xlsx" '
        print('ok')
        return response

