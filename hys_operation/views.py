from hys_operation.models import *
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
import json
import string
import random


def get_sub_users(request, obj_id):
    # 查找此服务器id下的帐号
    users = CoDicData.objects.filter(parent_id=obj_id).order_by('seq')
    result = []
    for i in users:
        # 对应的id和服务器帐号组成一个字典
        result.append({'id': i.id, 'name': i.dic_name})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_servers(request, obj_id):
    # 查找此机房id下的服务器
    servers = MachineInfo.objects.filter(idc=obj_id).order_by('-machine_ip')
    print(servers)
    result = []
    for i in servers:
        # 对应的id和服务器ip组成一个字典
        result.append({'id': i.id, 'name': i.machine_ip})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_web_machines(request, obj_id):
    # 查找此机房id下的WEB服务器
    servers = MachineInfo.objects.filter(idc=obj_id, app_type='WEB').order_by('-machine_ip')
    print(servers)
    result = []
    for i in servers:
        # 对应的id和服务器帐号组成一个字典
        result.append({'id': i.id, 'name': i.machine_ip})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_db_machines(request, obj_id):
    # 查找此机房id下的WEB服务器
    servers = MachineInfo.objects.filter(idc=obj_id, app_type='DB').order_by('-machine_ip')
    result = []
    for i in servers:
        # 对应的id和服务器帐号组成一个字典
        result.append({'id': i.id, 'name': i.machine_ip})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_de_users(request, obj_id):
    # 查找此项目id下的开发负责人
    users = Project.objects.get(pk=obj_id).de_charge.all()
    result = []
    for i in users:
        # 对应的id和姓名组成一个字典
        result.append({'id': i.pk, 'name': i.user_name})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_fde_users(request, obj_id):
    # 查找此项目id下的非开发负责人
    users = Project.objects.get(pk=obj_id).fde_charge.all()
    result = []
    for i in users:
        # 对应的id和姓名组成一个字典
        result.append({'id': i.pk, 'name': i.user_name})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_sub_pro_types(request, obj_id):
    # 查找此项目归属id下的项目
    pros = Project.objects.filter(project_type_id=obj_id)
    result = []
    for i in pros:
        # 对应的id和服务器帐号组成一个字典
        print(type(i.domain_name))
        result.append({'id': i.pk, 'name': i.domain_name})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def download(request, paper_num):
    """
    下载数据备案单
    :param request: 
    :param paper_num: 备案单号
    :return: 数据流
    """
    file_path = '/webserver/hys_cmdb/static/download/'
    # file_path = 'E:\\myweb\\hys_cmdb\\static\\download\\'
    file = open("{}{}.docx".format(file_path, paper_num), "rb")
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}.docx"'.format(paper_num)
    return response


def make_pwd(request, size=16, chars=string.ascii_lowercase+string.ascii_uppercase+string.digits):
    pwd = ''.join(random.choice(chars) for _ in range(size))
    request.session['new_pwd'] = pwd
    return HttpResponseRedirect('/')

