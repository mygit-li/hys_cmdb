from hys_operation.models import *
from django.http import HttpResponse
import json
from django.http import FileResponse


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
    # 查找此服务器id下的帐号
    servers = MachineInfo.objects.filter(idc=obj_id).order_by('-machine_ip')
    print(servers)
    result = []
    for i in servers:
        # 对应的id和服务器帐号组成一个字典
        result.append({'id': i.id, 'name': i.machine_ip})
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

