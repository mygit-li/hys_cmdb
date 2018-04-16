#!/usr/bin/env python
# Version = 3.5.2
# __auth__ = '无名小妖'
from django.contrib import admin
from hys_operation.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import (redirect, reverse)
from django.core.urlresolvers import reverse


class MyAdminSite(admin.AdminSite):
    site_header = '好医生运维资源管理系统'  # 此处设置页面显示标题
    site_title = '好医生运维'

admin_site = MyAdminSite(name='management')


class RecordAdmin(admin.ModelAdmin):
    change_form_template = 'admin/extras/record_change_form.html'

    def copy_current_data(self, obj):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        dest = '{}copy/'.format(obj.pk)
        title = '复制'
        return '<a href="{}">{}</a>'.format(dest, title)
    copy_current_data.short_description = '复制'
    copy_current_data.allow_tags = True

    def get_urls(self):
        """添加一个url，指向实现复制功能的函数copy_data"""
        from django.conf.urls import url
        urls = [
            url('^(?P<pk>\d+)copy/?$',
                self.admin_site.admin_view(self.copy_data),
                name='copy_data'),
        ]
        return urls + super(RecordAdmin, self).get_urls()

    def copy_data(self, request, *args, **kwargs):
        """函数实现复制本条数据，并跳转到新复制的数据的修改页面"""
        obj = get_object_or_404(Record, pk=kwargs['pk'])
        old_data = {'go_time': obj.go_time,
                    'machine_room_id': obj.machine_room_id,
                    'temperature': obj.temperature,
                    'humidity': obj.humidity,
                    'net': obj.net,
                    'trouble': obj.trouble,
                    'server_ip_id': obj.server_ip_id,
                    'trouble_type_id': obj.trouble_type_id,
                    'handle': obj.handle,
                    'mark': obj.mark,
                    'act_man': obj.act_man,
                    }

        r_pk = Record.objects.create(**old_data)
        co_path = request.path.split('/')
        co_path[-2] = "{}/change".format(r_pk)
        new_path = '/'.join(co_path)
        return redirect(new_path)

    def get_actions(self, request):
        actions = super(RecordAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def copy_one(self, request, queryset):
        # 定义actions函数
        # 判断用户选择了几条数据，如果是一条以上，则报错
        if queryset.count() == 1:
            old_data = queryset.values()[0]
            old_data.pop('id')
            # 将原数据复制并去掉id字段后插入数据库，以实现复制数据功能，返回值即新数据的id（这是在model里__str__中定义的）
            r_pk = Record.objects.create(**old_data)
            # 修改数据后重定向url到新加数据页面
            return HttpResponseRedirect('{}{}/change'.format(request.path, r_pk))
        else:
            self.message_user(request, "只能选取一条数据！")
    copy_one.short_description = "复制所选数据"

    actions = ['copy_one']
    list_display = ('go_time', 'server_ip_id', 'trouble_type_id', 'trouble', 'handle', 'net', 'mark', 'machine_room_id',
                    'temperature', 'humidity', 'act_man', 'copy_current_data')
    fk_fields = ('machine_room_id', 'act_man')
    list_per_page = 10
    list_filter = ('trouble_type_id__part_type_name', 'machine_room_id__machine_room_name')
    # list_editable = ['machine_room_id', 'temperature', 'humidity', 'trouble', 'handle', 'net', 'mark', 'act_man']
    ordering = ('-go_time',)
    search_fields = ('server_ip_id__machine_ip', 'trouble_type_id__part_type_name', 'mark')  # 搜索字段
    fieldsets = [
                    (None,	{
                        'classes': ('extrapretty', ),
                        'fields': [('act_man', 'machine_room_id', 'go_time')]
                    }),
                    ('详细信息', {'fields': [('server_ip_id', 'trouble_type_id'), 'trouble', 'handle', 'net',
                                         ('temperature', 'humidity'), 'mark']})
                    ]
    date_hierarchy = 'go_time'


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_mobile', 'user_job', 'privilege', 'mgr', 'pro_belong')
    fk_fields = ('user_job', )
    list_per_page = 15
    list_filter = ('mgr', 'pro_belong__project_type_name')
    search_fields = ('user_name', 'user_mobile')
    list_editable = ['user_email', 'user_mobile', 'user_job']
    fieldsets = [
                    ('负责人信息*',	{'fields': ['user_name', 'user_email', 'user_mobile', ]}),
                    ('其他信息', {'fields': ['user_job', 'privilege', 'mgr', 'pro_belong']})
                    ]


class UserJobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'department')
    list_per_page = 15
    list_filter = ('department', )
    list_editable = ('department',)


class PartTypeAdmin(admin.ModelAdmin):
    list_display = ('part_type_name', )
    list_per_page = 15
    list_filter = ('part_type_name', )


class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name',)
    list_per_page = 15


class CoDicTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name',)
    list_per_page = 15
    ordering = ('id', )


class CoDicDataAdmin(admin.ModelAdmin):
    list_display = ('dic_name', 'type')
    list_filter = ('type__type_name',)
    list_per_page = 15
    ordering = ('type', 'seq')


class MachineRoomAdmin(admin.ModelAdmin):
    list_display = ('machine_room_name', 'city_belonged')
    list_per_page = 15
    fk_fields = ('city_belonged',)
    list_filter = ('city_belonged__city_name',)


class MachineInfoAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ('machine_ip', 'status', 'user', 'machine_model', 'cache', 'app_type', 'mapping_ip',
                                    'band_width', 'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')

        return self.readonly_fields

    def get_list_filter(self, request):
        """  重新定义此函数，限制普通用户过滤功能  """
        if request.user.is_superuser or \
                        UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            self.list_filter = ('idc', 'status', 'machine_group__group_name', 'app_type')
        else:
            self.list_filter = ()
            
        return self.list_filter

    def get_queryset(self, request):
        """函数作用：使普通用户只能看到自己负责的服务器,总监可以看到组内所有服务器,管理员可见所有"""
        qs = super(MachineInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            groups = AuthUserGroups.objects.filter(user_id=request.user.id).values_list('group_id')
            return qs.filter(machine_group__in=groups)
        else:
            return qs.filter(user=UserInfo.objects.filter(user_name=request.user))

    def get_actions(self, request):
        """函数作用：使普通用户界面不显示动做按钮,管理员可以"""
        # actions = super().get_actions(request)
        if request.user.is_superuser or \
                        UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            actions = super().get_actions(request)
        else:
            actions = None
        return actions

    def has_add_permission(self, request):
        """函数作用：使普通用户界面不显示添加按钮,管理员可以"""
        if request.user.is_superuser or \
                        UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        """函数作用：使普通用户界面不显示删除按钮,管理员可以"""
        if request.user.is_superuser or \
                        UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            return True
        else:
            return False

    # by_ip.admin_order_field = 'by_ip'
    fieldsets = [
        (None, {'fields': [('machine_ip', 'mapping_ip', 'machine_model', 'machine_os', 'application', 'app_type')]}),
        ('硬信息*', {'fields': [('cache', 'cpu', 'hard_disk', 'status', 'band_width')]}),
        ('软信息*', {'fields': [('user', 'idc', 'machine_group'), ('os_user', 'os_pwd'), 'os_mark']})
    ]
    list_display = ('machine_ip', 'application', 'colored_status', 'user', 'machine_model', 'cache',
                    'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group', )
    # list_per_page = 15
    # list_filter = ('status', 'user__user_name', 'machine_group__group_name')
    fk_fields = ('user', 'idc', 'machine_group')
    search_fields = ('machine_ip', 'application')  # 搜索字 段
    ordering = ('-idc', )
    list_select_related = ('user', 'idc')
    # readonly_fields = ('machine_ip', 'status', 'user', 'machine_model', 'cache', 'os_user',
    #                      'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')


class DataPaperStoreAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        """函数作用：使普通用户只能看见部分字段,管理员可见所有"""
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': [('project_name', 'to_mail'), 'data_selected',
                                                 ('proposer', 'frequency')]}),
                              (None, {'fields': [('commit_date', 'start_date', 'end_date',), 'sql']}),
                              (None, {'fields': [('paper_num', 'is_sure', 'is_expired'), 'mark']}),)
        else:
            self.fieldsets = ((None, {'fields': ('project_name', 'to_mail', 'data_selected', 'frequency',
                                                 'start_date', 'end_date', 'is_expired', ), }),)
        return super(DataPaperStoreAdmin, self).get_form(request, obj=None, **kwargs)

    def get_queryset(self, request):
        """函数作用：使普通用户只能看到自己负责的数据胆,管理员可见所有"""
        qs = super(DataPaperStoreAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(proposer=request.user)

    def has_delete_permission(self, request, obj=None):
        """函数作用：使普通用户界面不显示删除按钮,管理员可以"""
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_actions(self, request):
        """函数作用：使普通用户界面不显示动做按钮,管理员可以"""
        # actions = super().get_actions(request)
        if request.user.is_superuser:
            actions = super().get_actions(request)
        else:
            actions = None
        return actions

    def get_list_display(self, request):
        """  重新定义此函数，限制普通用户过滤功能  """
        if request.user.is_superuser:
            self.list_filter = ('proposer', 'commit_date', 'paper_num')
        else:
            self.list_filter = ()

        return self.list_display

    def save_model(self, request, obj, form, change):
        """  重新定义此函数，提交时自动添加申请人和备案号  """

        def make_paper_num():
            """ 生成随机备案号 """
            import datetime
            import random
            current_time = datetime.datetime.now().strftime("%Y-%m-%d")  # 生成当前时间
            random_num1 = random.randint(11, 100)  # 生成的随机整数n，其中11<=n<=100
            random_num2 = random.randint(11, 100)  # 生成的随机整数n，其中11<=n<=100
            unique_num = '好医生数调备字【{}-{}-{}】'.format(current_time, random_num1, random_num2)
            return unique_num

        if request.user.is_superuser:
            super(DataPaperStoreAdmin, self).save_model(request, obj, form, change)
        elif obj.proposer:
            super(DataPaperStoreAdmin, self).save_model(request, obj, form, change)
        else:
            obj.proposer = request.user
            obj.paper_num = make_paper_num()
            super(DataPaperStoreAdmin, self).save_model(request, obj, form, change)

    def get_list_filter(self, request):
        """  重新定义此函数，取消过滤功能  """
        self.list_filter = ()
        return self.list_filter

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = ['commit_date', 'is_expired', ]
        elif hasattr(obj, 'is_sure'):
            if obj.is_sure:
                self.readonly_fields = ('project_name', 'to_mail', 'data_selected', 'frequency', 'start_date',
                                        'end_date', 'is_expired',)
        else:
            self.readonly_fields = ('paper_num', 'is_sure', 'proposer', 'sql', 'commit_date', 'is_expired',)

        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        change_obj = DataPaperStore.objects.filter(pk=object_id)
        self.get_readonly_fields(request, obj=change_obj)
        return super(DataPaperStoreAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def expired(self, ps):
        """自定义列表字段, 根据数据单截止日期和当前日期判断是否过期,并对数据库进行更新"""
        import datetime
        from django.utils.html import format_html
        end_date = ps.end_date
        if end_date >= datetime.date.today():
            ret = '未过期'
            color_code = 'green'
        else:
            ret = '已过期'
            color_code = 'red'
        DataPaperStore.objects.filter(pk=ps.pk).update(is_expired=ret)
        return format_html(
                    '<span style="color: {};">{}</span>',
                    color_code,
                    ret,
                )
    expired.short_description = '是否已过期'
    expired.admin_order_field = 'end_date'

    def down_paper(self, obj):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        dest = '{}export/'.format(obj.pk)
        title = '下载'
        return '<a href="{}">{}</a>'.format(dest, title)
    down_paper.short_description = '下载数据单'
    down_paper.allow_tags = True

    def get_urls(self):
        """添加一个url，指向实现复制功能的函数copy_one"""
        from django.conf.urls import url
        urls = [
            url('^(?P<pk>\d+)export/?$',
                self.admin_site.admin_view(self.make_docx),
                name='export_data'),
        ]
        return urls + super(DataPaperStoreAdmin, self).get_urls()

    def make_docx(self, request, *args, **kwargs):
        from docxtpl import DocxTemplate
        import re
        # file_path = 'E:\\myweb\\hys_cmdb\\static\\download\\'
        file_path = '/webserver/hys_cmdb/static/download/'
        obj = get_object_or_404(DataPaperStore, pk=kwargs['pk'])
        list_nums = re.findall("\d+", obj.paper_num)  # 获取字符串中的所有数字
        nums = ''.join(list_nums)
        doc = DocxTemplate("{}export.docx".format(file_path))
        context = {'paper_num': obj.paper_num,
                   'project_name': obj.project_name,
                   'to_mail': obj.to_mail,
                   'data_selected': obj.data_selected,
                   'start_date': obj.start_date,
                   'end_date': obj.end_date,
                   }
        doc.render(context)
        doc.save("{}{}.docx".format(file_path, nums))
        new_path = reverse('download', args=(nums,))
        return HttpResponseRedirect(new_path)

    list_display = ('project_name', 'to_mail', 'proposer', 'frequency', 'commit_date',
                    'start_date', 'end_date', 'colored_paper_num', 'is_sure', 'expired', 'down_paper',)
    list_per_page = 15
    search_fields = ('proposer', 'paper_num')
    ordering = ['-end_date', ]


class DailyReportDbaAdmin(admin.ModelAdmin):

    # A template for a very customized change view:
    change_form_template = 'admin/extras/reportdba_change_form.html'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     return super(DailyReportDbaAdmin, self).change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )
    # def get_actions(self, request):
    #     actions = super(DailyReportDbaAdmin, self).get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    # def copy_one(self, request, queryset):
    #     # 定义actions函数
    #     # 判断用户选择了几条数据，如果是一条以上，则报错
    #     if queryset.count() == 1:
    #         old_data = queryset.values()[0]
    #         old_data.pop('id')
    #         # 将原数据复制并去掉id字段后，插入数据库，以实现复制数据功能，返回值即新数据的id（这是在model里__str__中定义的）
    #         r_pk = DailyReportDba.objects.create(**old_data)
    #         # 修改数据后重定向url到新加数据页面
    #         # return HttpResponseRedirect('{}{}/change'.format(request.path, r_pk))
    #         return redirect('{}{}/change'.format(request.path, r_pk))
    #     else:
    #         self.message_user(request, "只能选取一条数据！")
    # copy_one.short_description = "复制所选数据"

    def copy_current_data(self, obj):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        dest = '{}copy/'.format(obj.pk)
        title = '复制'
        return '<a href="{}">{}</a>'.format(dest, title)
    copy_current_data.short_description = '复制'
    copy_current_data.allow_tags = True

    def get_urls(self):
        """添加一个url，指向实现复制功能的函数copy_one"""
        from django.conf.urls import url
        urls = [
            url('^(?P<pk>\d+)copy/?$',
                self.admin_site.admin_view(self.copy_one),
                name='copy_data'),
        ]
        return urls + super(DailyReportDbaAdmin, self).get_urls()

    def copy_one(self, request, *args, **kwargs):
        """函数实现复制本条数据，并跳转到新复制的数据的修改页面"""
        obj = get_object_or_404(DailyReportDba, pk=kwargs['pk'])
        old_data = {'create_date': obj.create_date,
                    'db_server': obj.db_server,
                    'db_user': obj.db_user,
                    'request_type': obj.request_type,
                    'request': obj.request,
                    'scripts': obj.scripts,
                    'de_proposer': obj.de_proposer,
                    'fde_proposer': obj.fde_proposer,
                    'operator': obj.operator,
                    'is_complete': obj.is_complete,
                    'remark': obj.remark,
                    }

        r_pk = DailyReportDba.objects.create(**old_data)
        co_path = request.path.split('/')
        co_path[-2] = "{}".format(r_pk)
        new_path = '/'.join(co_path)
        return redirect(new_path)

    # actions = ['copy_one']
    fieldsets = [
        ('时间和服务器*', {'fields': [('create_date', 'db_server', 'db_user')]}),
        ('需求和脚本*', {'fields': ['request_type', 'request', 'scripts']}),
        ('申请人和操作人*', {'fields': [('de_proposer', 'fde_proposer', 'operator', 'is_complete'), 'remark']})
    ]
    list_display = ('create_date', 'db_server', 'db_user', 'request', 'request_type',
                    'de_proposer', 'fde_proposer', 'operator', 'is_complete', 'copy_current_data', )
    list_per_page = 10
    # list_filter = ('db_server__dic_name', 'request_type__dic_name', 'operator__dic_name', 'proposer__dic_name')
    # list_editable = ['machine_room_id', 'temperature', 'humidity', 'trouble', 'handle', 'net', 'mark', 'act_man']
    search_fields = ('db_server__dic_name', 'db_user__dic_name', 'request', 'request_type__dic_name',
                     'operator__dic_name', 'de_proposer__dic_name', 'fde_proposer__dic_name')
    date_hierarchy = 'create_date'
    ordering = ['-create_date', ]


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('project_type_name',)
    list_per_page = 10


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'project_name', 'project_type', 'create_date', )
    filter_horizontal = ('fde_charge', 'de_charge',)
    list_per_page = 15
    list_filter = ('project_name', )
    search_fields = ('domain_name',)


class DailyReportOsaAdmin(admin.ModelAdmin):
    change_form_template = 'admin/extras/reportosa_change_form.html'

    def copy_current_data(self, obj):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        dest = '{}copy/'.format(obj.pk)
        title = '复制'
        return '<a href="{}">{}</a>'.format(dest, title)
    copy_current_data.short_description = '复制'
    copy_current_data.allow_tags = True

    def get_urls(self):
        """添加一个url，指向实现复制功能的函数copy_one"""
        from django.conf.urls import url
        urls = [
            url('^(?P<pk>\d+)copy/?$',
                self.admin_site.admin_view(self.copy_one),
                name='copy_os_data'),
        ]
        return urls + super(DailyReportOsaAdmin, self).get_urls()

    def copy_one(self, request, *args, **kwargs):
        """函数实现复制本条数据，并跳转到新复制的数据的修改页面"""
        obj = get_object_or_404(DailyReportOsa, pk=kwargs['pk'])
        old_data = {'create_date': obj.create_date,
                    'project_type': obj.project_type,
                    'project': obj.project,
                    'web_server': obj.web_server,
                    'db_server': obj.db_server,
                    'operations': obj.operations,
                    'de_proposer': obj.de_proposer,
                    'fde_proposer': obj.fde_proposer,
                    'operator': obj.operator,
                    'scripts': obj.scripts,
                    'is_complete': obj.is_complete,
                    'remark': obj.remark,
                    }

        r_pk = DailyReportOsa.objects.create(**old_data)
        co_path = request.path.split('/')
        co_path[-2] = "{}".format(r_pk)
        new_path = '/'.join(co_path)
        return redirect(new_path)

    # actions = ['copy_one']
    fieldsets = [
        ('时间和项目*', {'fields': [('create_date', 'project_type', 'project', )]}),
        ('服务器信息*', {'fields': [('machine_room_id', 'web_server', 'db_server')]}),
        ('操作类型和命令*', {'fields': ['operations', 'scripts']}),
        ('申请人和操作人*', {'fields': [('de_proposer', 'fde_proposer', 'operator', 'is_complete'), 'remark']})
    ]
    list_display = ('create_date', 'project_type', 'project', 'machine_room_id', 'web_server', 'db_server',
                    'operations', 'de_proposer', 'fde_proposer', 'operator', 'is_complete', 'copy_current_data')
    list_per_page = 10
    # list_filter = ('db_server__dic_name', 'request_type__dic_name', 'operator__dic_name', 'proposer__dic_name')
    # search_fields = ('db_server__dic_name', 'db_user__dic_name', 'request', 'request_type__dic_name',
    #                  'operator__dic_name', 'de_proposer__dic_name', 'fde_proposer__dic_name')
    date_hierarchy = 'create_date'
    ordering = ['-create_date', ]

admin_site.register(Record, RecordAdmin)
admin_site.register(UserInfo, UserInfoAdmin)
admin_site.register(UserJob, UserJobAdmin)
admin_site.register(City, CityAdmin)
admin_site.register(MachineRoom, MachineRoomAdmin)
admin_site.register(MachineInfo, MachineInfoAdmin)
admin_site.register(DataPaperStore, DataPaperStoreAdmin)
admin_site.register(PartType, PartTypeAdmin)
admin_site.register(CoDicType, CoDicTypeAdmin)
admin_site.register(CoDicData, CoDicDataAdmin)
admin_site.register(DailyReportDba, DailyReportDbaAdmin)
admin_site.register(DailyReportOsa, DailyReportOsaAdmin)
admin_site.register(ProjectType, ProjectTypeAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(MachineGroup)


