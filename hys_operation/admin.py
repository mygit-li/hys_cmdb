from django.contrib import admin
from hys_operation.models import *


class MyAdminSite(admin.AdminSite):
    site_header = '好医生运维资源管理系统'  # 此处设置页面显示标题
    site_title = '好医生运维'

admin_site = MyAdminSite(name='management')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('go_time', 'net', 'server', 'trouble', 'mark', 'machine_room_id',
                    'temperature', 'humidity', 'act_man')
    fk_fields = ('machine_room_id', 'act_man')
    list_per_page = 10
    list_filter = ('trouble', 'go_time', 'act_man__user_name', 'machine_room_id__machine_room_name')
    list_editable = ['machine_room_id', 'temperature', 'humidity', 'net', 'server', 'trouble', 'mark', 'act_man']
    ordering = ('-go_time',)
    search_fields = ('server', 'net', 'mark')  # 搜索字段
    fieldsets = [
                    (None,	{'fields': ['act_man', 'machine_room_id']}),
                    ('巡检时间*',  {'fields': ['go_time']}),
                    ('详细信息', {'fields': ['temperature', 'humidity', 'net', 'server', 'trouble', 'mark']})
                    ]
    date_hierarchy = 'go_time'


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_mobile', 'user_job', 'privilege')
    fk_fields = ('user_job', )
    list_per_page = 15
    list_filter = ('user_name', 'user_mobile')
    list_editable = ['user_email', 'user_mobile', 'user_job']
    fieldsets = [
                    ('负责人*',	{'fields': ['user_name']}),
                    ('其他信息', {'fields': ['user_email', 'user_mobile', 'user_job', 'privilege']})
                    ]


class UserJobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'department')
    list_per_page = 15
    list_filter = ('department', )
    list_editable = ('department',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name',)
    list_per_page = 15


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
            self.readonly_fields = ('machine_ip', 'status', 'user', 'machine_model', 'cache',
                                    'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')

        return self.readonly_fields

    def get_list_filter(self, request):
        """  重新定义此函数，限制普通用户过滤功能  """
        if request.user.is_superuser or \
                        UserInfo.objects.filter(user_name=request.user).values_list('privilege')[0][0] == 1:
            self.list_filter = ('status', 'user__user_name', 'machine_group__group_name')
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
        actions = super().get_actions(request)
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

    list_display = ('machine_ip', 'application', 'colored_status', 'user', 'machine_model', 'cache',
                    'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')
    # list_per_page = 15
    # list_filter = ('status', 'user__user_name', 'machine_group__group_name')
    fk_fields = ('user', 'idc', 'machine_group')
    search_fields = ('machine_ip', 'application')  # 搜索字 段
    ordering = ('machine_ip',)
    list_select_related = ('user', 'idc')
    # readonly_fields = ('machine_ip', 'status', 'user', 'machine_model', 'cache', 'os_user',
    #                      'cpu', 'hard_disk', 'machine_os', 'idc', 'machine_group')


class DataPaperStoreAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('project_name', 'to_mail', 'data_selected', 'proposer', 'frequency',
                                                 'commit_date', 'start_date', 'end_date', 'paper_num', 'sql',
                                                 'is_sure'), }),)
        else:
            self.fieldsets = ((None, {'fields': ('project_name', 'to_mail', 'data_selected', 'frequency',
                                                 'start_date', 'end_date', ), }),)
        return super(DataPaperStoreAdmin,self).get_form(request, obj=None, **kwargs)

    def get_queryset(self, request):
        """函数作用：使普通用户只能看到自己负责的服务器,管理员可见所有"""
        qs = super(DataPaperStoreAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(proposer=request.user)

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = ['commit_date', 'paper_num']
        else:
            self.readonly_fields = ('paper_num', 'is_sure', 'proposer', 'sql', 'commit_date')

        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        """函数作用：使普通用户界面不显示删除按钮,管理员可以"""
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_actions(self, request):
        """函数作用：使普通用户界面不显示动做按钮,管理员可以"""
        actions = super().get_actions(request)
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
            CurrentTime = datetime.datetime.now().strftime("%Y-%m-%d")  # 生成当前时间
            RandomNum1 = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
            RandomNum2 = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
            UniqueNum = '好医生数调备字【{}-{}-{}】'.format(CurrentTime, RandomNum1, RandomNum2)
            return UniqueNum

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

    list_display = ('project_name', 'to_mail', 'proposer', 'frequency', 'commit_date',
                    'start_date', 'end_date','paper_num', 'is_sure')
    list_per_page = 15
    search_fields = ('proposer', 'paper_num')


admin_site.register(Record, RecordAdmin)
admin_site.register(UserInfo, UserInfoAdmin)
admin_site.register(UserJob, UserJobAdmin)
admin_site.register(City, CityAdmin)
admin_site.register(MachineRoom, MachineRoomAdmin)
admin_site.register(MachineInfo, MachineInfoAdmin)
admin_site.register(DataPaperStore, DataPaperStoreAdmin)
admin_site.register(MachineGroup)

