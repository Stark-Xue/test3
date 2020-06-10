from django.shortcuts import render, HttpResponse, redirect
from cmdb import models
import json

# Create your views here.

def business(request):
    # way one
    v1 = models.Business.objects.all()
    # QuerySet, 内部元素是对象
    # [obj(id, caption, code), obj, obj...]

    # way two
    v2 = models.Business.objects.all().values('id', 'caption')
    # QuerySet, 内部元素是字典
    # [{'id':1, 'caption':'运维部'},{},{}...]

    # way three
    v3 = models.Business.objects.all().values_list('id', 'caption')
    # QuerySet, 内部元素是元组
    # [(1, '运维部'),(2, '开发'),()...]

    return render(request, "business.html", {"v1": v1, 'v2': v2, 'v3': v3})

# def host(request):
#     v1 = models.Host.objects.all()
#     for row in v1:
#         print(row.nid, row.hostname, row.ip, row.port, row.b_id, row.b)

#     v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'ip', 'port', 'b_id', 'b__caption')
#     print(v2)
#     for row in v2:
#         print(row['nid'], row['hostname'], row['b__caption'])

#     v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'ip', 'port', 'b_id', 'b__caption')


#     return render(request, 'host.html', {'v1': v1, 'v2': v2, 'v3': v3})

def host(request):
    if request.method == "GET":
        v1 = models.Host.objects.all()
        v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'ip', 'port', 'b_id', 'b__caption')
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'ip', 'port', 'b_id', 'b__caption')
        b_list = models.Business.objects.all()

        for row in v2:
            print(row["nid"],row["hostname"],row["ip"],row["port"],row["b_id"],row["b__caption"])

        return render(request, 'host.html', {'v1': v1, 'v2': v2, 'v3': v3, 'b_list': b_list})
    elif request.method == "POST":
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        # models.Host.objects.create(hostname=h,
        #                             ip=i,
        #                             port=p,
        #                             b=models.Business.objects.get(id=b)
        #                             )
        models.Host.objects.create(hostname=h,
                                    ip=i,
                                    port=p,
                                    b_id=b
                                    )
        return redirect('/host')

def test_ajax(request):
    ret = {"status": True, "error": None, "data": None}
    try:
        print(request.method, request.POST, sep="\t")
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                            ip=i,
                                            port=p,
                                            b_id=b)
        else:
            ret['status'] = False
            ret['error'] = '太短了'
    except Exception as e:
        ret['status'] = False
        ret['error'] = '请求错误'
    return HttpResponse(json.dumps(ret))

def app(request):
    if request.method == "GET":
        app_list = models.Application.objects.all()
        host_list = models.Host.objects.all()
        '''
        app_list = models.Application.objects.all()
        app_list.name

        app_list.r.add(1)
        app_list.r.add(2)
        app_list.r.add(3,4,5)
        app_list.r.add(*[1,2,3,4])

        app_list.r.remove(1)
        app_list.r.remove(2,3)
        app_list.r.remove(*[1,2,3])

        app_list.r.clear()

        app_list.r.set([3,4,5]) # 清空之前的所有，变成我现在设置的这个

        app_list.r.all() # 所有相关的主机对象"列表" QuerySet
        '''
        for row in app_list:
            print(row.name, row.r.all())
        return render(request, 'app.html', {'app_list': app_list, 'host_list': host_list})
    elif request.method == "POST":
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        print(app_name, host_list)
        obj = models.Application.objects.create(name=app_name) # 创建成功，返回刚创建的这个对象
        obj.r.add(*host_list)
        return redirect("/app")

def ajax_add_app(request):
    ret = {"status": True, "error": None, 'data': None}
    print(request.POST.get('app_name'))
    print(request.POST.getlist('host_list'))
    app_name = request.POST.get('app_name')
    host_list = request.POST.getlist('host_list')
    obj = models.Application.objects.create(name=app_name)
    obj.r.add(*host_list)
    return HttpResponse(json.dumps(ret))