from django.db import models
from django.utils.html import format_html
from django.shortcuts import get_object_or_404


class CoDicType(models.Model):
    type_name = models.CharField(max_length=200, null=False, verbose_name=u"字典类型")
    type_code = models.CharField(max_length=2, null=False, verbose_name=u"字典编码")

    class Meta:
        db_table = 'co_dic_type'
        verbose_name = 'CO--字典类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.type_name)


class CoDicData(models.Model):
    dic_name = models.CharField(max_length=200, null=False, verbose_name=u"字典名称")
    seq = models.IntegerField(verbose_name=u"顺序号")
    type = models.ForeignKey('CoDicType', verbose_name=u"字典类型")
    parent_id = models.IntegerField(null=True, blank=True, verbose_name=u"上级id")

    class Meta:
        db_table = 'co_dic_data'
        unique_together = ('dic_name', 'type', 'parent_id')
        verbose_name = 'CO--字典表'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.type.type_code == 'sv':
            return "{}【id:{}】".format(self.dic_name, self.pk)
        else:
            return str(self.dic_name)


class UserJob(models.Model):
    """职位表"""
    job_name = models.CharField(max_length=40, verbose_name=u"职位")             # 职位
    department = models.ForeignKey('MachineGroup', verbose_name=u"部门")            # 部门

    class Meta:
        db_table = 'user_job'
        verbose_name = 'CO--职位表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job_name


class UserInfo(models.Model):
    """用户表"""
    user_name = models.CharField(max_length=20, unique=True, verbose_name=u"负责人")         # 负责人
    user_email = models.EmailField(null=True, blank=True, verbose_name=u"邮箱")     # 邮箱
    user_mobile = models.BigIntegerField(verbose_name=u"电话")                 # 电话
    user_job = models.ForeignKey('UserJob', verbose_name=u"职位")         # 职位id
    status_choice = (
        (0, '普通权限'),
        (1, '高级权限'),
    )
    privilege = models.IntegerField(choices=status_choice, default=0, verbose_name='显示权限', db_column='privilege')
    mgr = models.ForeignKey('UserInfo', default=1, verbose_name='上级')
    pro_belong = models.ForeignKey('ProjectType', default=1, verbose_name='项目归属')

    class Meta:
        db_table = 'user_info'
        verbose_name = 'AA--用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class City(models.Model):
    """城市分布表"""
    city_name = models.CharField(max_length=40, verbose_name=u"城市名称")         # 城市名称

    class Meta:
        db_table = 'city'
        verbose_name = 'CO--城市分布表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city_name


class MachineRoom(models.Model):
    """机房信息表"""
    machine_room_name = models.CharField(max_length=40, verbose_name=u"机房名称")                 # 机房名称
    city_belonged = models.ForeignKey('City', verbose_name=u"所属城市")                     # 所属城市id

    class Meta:
        db_table = 'machine_room'
        verbose_name = 'CO--机房信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.machine_room_name


class MachineGroup(models.Model):
    """主机所属组"""
    group_name = models.CharField(max_length=40, verbose_name=u"组名称")        # 组名称

    class Meta:
        db_table = 'machine_group'
        verbose_name = 'CO--主机属组表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


class MachineInfo(models.Model):
    """主机信息表"""
    machine_model = models.CharField(max_length=40, verbose_name=u"型号")        # 型号
    machine_ip = models.CharField(max_length=100, unique=True, verbose_name=u"ip地址")           # ip
    mapping_ip = models.CharField(max_length=40, blank=True, null=True, db_column='mapping_ip', verbose_name=u"映射ip")
    cache = models.CharField(max_length=12, verbose_name=u"内存")                # 内存
    cpu = models.CharField(max_length=4, verbose_name=u"cpu")                   # cpu
    hard_disk = models.CharField(max_length=200, verbose_name=u"磁盘")            # 磁盘大小
    os_type_id = get_object_or_404(CoDicType, type_code='xt').pk
    machine_os = models.ForeignKey(CoDicData, related_name='machine_os', limit_choices_to={'type_id': os_type_id},
                                   verbose_name='操作系统')
    application = models.CharField(max_length=600, verbose_name=u"用途")         # 用途
    
    bandwidth_id = get_object_or_404(CoDicType, type_code='dk').pk
    band_width = models.ForeignKey(CoDicData, related_name='bandwidth', limit_choices_to={'type': bandwidth_id},
                                   db_column='band_width', default=228, verbose_name='带宽')
    app_choices = (
        ('WEB', 'WEB'),
        ('DB', 'DB'),
    )
    app_type = models.CharField(max_length=8, choices=app_choices, default='WEB', verbose_name=u"应用类型") 
    status_choices = (
        ('正常', '正常'),
        ('损坏', '损坏'),
    )
    status = models.CharField(max_length=8, choices=status_choices, verbose_name=u"状态")    # 状态

    user = models.ForeignKey('UserInfo', verbose_name=u"负责人")     # 负责人
    idc = models.ForeignKey('MachineRoom', verbose_name=u"所属机房")    # 所属机房
    machine_group = models.ForeignKey('MachineGroup', verbose_name=u"所属组")     # 所属组
    os_user = models.CharField(null=True, max_length=30, verbose_name=u"主机用户名")  # 主机用户名
    os_pwd = models.CharField(null=True, max_length=40, verbose_name=u"密码")  # 密码
    os_mark = models.TextField(null=True, blank=True, max_length=600, verbose_name=u"备注")  # 备注

    class Meta:
        db_table = 'machine_info'
        verbose_name = 'AA--主机信息表'
        verbose_name_plural = verbose_name

    def colored_status(self):
        if self.status == '损坏':
            color_code = 'red'
        else:
            color_code = 'green'
        return format_html(
                    '<span style="color: {};">{}</span>',
                    color_code,
                    self.status,
                )

    colored_status.short_description = u"状态"

    def __str__(self):
        return self.machine_ip


class PartType(models.Model):
    """服务器配件类型表"""
    part_type_name = models.CharField(max_length=200, null=True, verbose_name="配件类型名称")

    class Meta:
        db_table = 'part_type'
        verbose_name = 'CO--服务器配件类型表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.part_type_name


class Record(models.Model):
    """巡检记录"""
    operator_type_id = get_object_or_404(CoDicType, type_code='hd').pk

    go_time = models.DateTimeField(null=True, verbose_name=u"巡检时间")  # 巡检时间
    machine_room_id = models.ForeignKey('MachineRoom', db_column='machine_room_id', verbose_name=u"所属机房")  # 机房id
    temperature = models.IntegerField(null=True, verbose_name=u"温度")  # 温度
    humidity = models.IntegerField(null=True, verbose_name=u"湿度")  # 湿度
    net = models.CharField(max_length=200, verbose_name=u"网络设备")  # 网络设备
    trouble = models.CharField(max_length=200, verbose_name=u"故障内容")  # 服务器
    server_ip_id = models.ForeignKey('MachineInfo', db_column='server_ip_id', verbose_name="服务器")
    trouble_type_id = models.ForeignKey('PartType', db_column='trouble_type_id', verbose_name="故障类型")
    handle = models.CharField(max_length=200, default='', verbose_name=u"故障处理")  # 故障处理
    mark = models.CharField(max_length=200, verbose_name=u"备注")  # 备注
    act_man = models.ForeignKey(CoDicData, related_name='act', limit_choices_to={'type_id': operator_type_id},
                                verbose_name='巡检人')

    class Meta:
        db_table = 'record'
        verbose_name = 'AA--巡检记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 此处返回数据的id，由于admin的actions的中的重定向功能要用到，所以不能修改
        return str(self.pk)


class AuthUserGroups(models.Model):
    """人员属组表"""
    user_id = models.IntegerField(verbose_name=u"用户id", db_column='user_id')
    group_id = models.IntegerField(verbose_name=u"属组id", db_column='group_id')

    class Meta:
        db_table = 'auth_user_groups'
        verbose_name = 'CO--人员属组关系表'
        verbose_name_plural = verbose_name
        managed = False


class DataPaperStore(models.Model):
    """数据单备案表"""
    project_name = models.CharField(max_length=100, verbose_name=u"项目归属")
    to_mail = models.EmailField(verbose_name=u"接收邮箱")
    data_selected = models.TextField(max_length=1000, verbose_name=u"数据选项")
    proposer = models.CharField(max_length=100, verbose_name=u"申请人")
    frequency = models.CharField(max_length=400, verbose_name=u"频率")
    commit_date = models.DateField(auto_now_add=True, verbose_name=u"申请时间")
    start_date = models.DateField(null=True, verbose_name=u"开始时间")
    end_date = models.DateField(null=True, verbose_name=u"结束时间")
    sql = models.TextField(max_length=100000, verbose_name=u"sql语句")
    paper_num = models.CharField(max_length=50, verbose_name=u"备案号")
    is_sure = models.BooleanField(default=False, verbose_name=u"是否已确认")
    is_expired = models.CharField(max_length=20, default='未过期', verbose_name=u"是否已过期")
    mark = models.TextField(max_length=10000, null=True, verbose_name=u"备注")

    class Meta:
        db_table = 'data_paper_store'
        verbose_name = 'AA--数据单备案表'
        verbose_name_plural = verbose_name

    def colored_paper_num(self):
        if self.paper_num:
            color_code = 'blue'
        else:
            color_code = 'red'
        return format_html(
                    '<span style="color: {};">{}</span>',
                    color_code,
                    self.paper_num,
                )

    colored_paper_num.short_description = u"备案号"

    def __str__(self):
        return self.project_name + '||' + self.paper_num


class DailyReportDba(models.Model):
    """
        "1"	"需求类型"	"rq"
        "2"	"处理人员"	"hd"
        "3"	"申请人员(开发)"	"po"
        "4"	"DB服务器"	"sv"
        "5"	"DB用户名"	"un"
        "6"	"申请人员(非开发)"	"fp"
    """
    server_type_id = get_object_or_404(CoDicType, type_code='sv').pk
    db_user_id = get_object_or_404(CoDicType, type_code='un').pk
    request_type_id = get_object_or_404(CoDicType, type_code='rq').pk
    proposer_de_id = get_object_or_404(CoDicType, type_code='po').pk
    operator_type_id = get_object_or_404(CoDicType, type_code='hd').pk
    operator_fde_id = get_object_or_404(CoDicType, type_code='fp').pk

    create_date = models.DateField(null=True, verbose_name="创建时间")
    db_server = models.ForeignKey(CoDicData, related_name='server', limit_choices_to={'type': server_type_id},
                                  default=66, verbose_name='DB服务器')
    db_user = models.ForeignKey(CoDicData, related_name='username', limit_choices_to={'type': db_user_id},
                                default=120, verbose_name='DB用户名')
    request = models.TextField(max_length=10000, null=True, verbose_name="需求")
    request_type = models.ForeignKey(CoDicData, related_name='re', limit_choices_to={'type_id': request_type_id},
                                     default=89, verbose_name='需求类型')
    de_proposer = models.ForeignKey(CoDicData, related_name='pro', limit_choices_to={'type_id': proposer_de_id},
                                    default=3, verbose_name='申请人(开发)')
    fde_proposer = models.ForeignKey(CoDicData, related_name='fpr', limit_choices_to={'type_id': operator_fde_id},
                                     default=56, verbose_name='申请人(非开发)')
    operator = models.ForeignKey(CoDicData, related_name='oper', limit_choices_to={'type_id': operator_type_id},
                                 default=2, verbose_name='操作人')
    scripts = models.TextField(max_length=10000, null=True, blank=True, verbose_name="脚本")
    is_complete = models.BooleanField(default=False, verbose_name="是否已完成")
    remark = models.TextField(max_length=10000, null=True, blank=True, verbose_name=u"备注")

    class Meta:
        db_table = 'daily_report_dba'
        verbose_name = 'AA--日志(DBA)'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pk)


class ProjectType(models.Model):
    project_type_name = models.CharField(max_length=2000, verbose_name=u"项目归属名称")

    class Meta:
        db_table = 'project_type'
        verbose_name = 'CO--项目归属'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_type_name


class Project(models.Model):
    domain_name = models.CharField(unique=True, max_length=200, verbose_name="域名")
    project_name = models.CharField(max_length=2000, verbose_name="项目名称")
    project_type = models.ForeignKey('ProjectType', related_name='gs', verbose_name='项目归属')
    project_head = models.ForeignKey('UserInfo', related_name='fz', verbose_name='项目负责人')
    fde_charge = models.ManyToManyField(UserInfo, related_name='nb', verbose_name='内部负责人')
    de_charge = models.ManyToManyField(UserInfo, related_name='kf', verbose_name='开发负责人')
    create_date = models.DateTimeField(verbose_name="创建时间")

    class Meta:
        db_table = 'project'
        verbose_name = 'AA--项目表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.domain_name


class DailyReportOsa(models.Model):
    """
        "8"	"项目"	"xm"
        "9"	"操作类型"	"cz"
        "2"	"处理人员"	"hd"
        "3"	"申请人员(开发)"	"po"
        "6"	"申请人员(非开发)"	"fp"
    """
    project_id = get_object_or_404(CoDicType, type_code='xm').pk
    oper_type_id = get_object_or_404(CoDicType, type_code='cz').pk
    proposer_de_id = get_object_or_404(CoDicType, type_code='po').pk
    operator_type_id = get_object_or_404(CoDicType, type_code='hd').pk
    proposer_fde_id = get_object_or_404(CoDicType, type_code='fp').pk

    create_date = models.DateField(null=True, verbose_name="创建时间")
    project_type = models.ForeignKey(ProjectType, default=1, verbose_name='项目归属')
    project = models.ForeignKey(Project, default=1, verbose_name='项目')
    # project = models.CharField(max_length=400, verbose_name='项目')
    machine_room_id = models.ForeignKey('MachineRoom', db_column='machine_room_id', default=3,
                                        verbose_name=u"所属机房")
    web_server = models.ForeignKey(MachineInfo, related_name='web_server', limit_choices_to={'app_type': 'WEB'},
                                   null=True, verbose_name='WEB服务器')
    db_server = models.ForeignKey(MachineInfo, related_name='db_server', limit_choices_to={'app_type': 'DB'},
                                  null=True, verbose_name='DB服务器')
    operations = models.ForeignKey(CoDicData, related_name='op', limit_choices_to={'type_id': oper_type_id},
                                   null=True, verbose_name='操作类型')
    de_proposer = models.ForeignKey(CoDicData, related_name='de', limit_choices_to={'type_id': proposer_de_id},
                                    null=True, verbose_name='申请人(开发)')
    fde_proposer = models.ForeignKey(CoDicData, related_name='fde', limit_choices_to={'type_id': proposer_fde_id},
                                     null=True, verbose_name='申请人(非开发)')
    operator = models.ForeignKey(CoDicData, related_name='opt', limit_choices_to={'type_id': operator_type_id},
                                 null=True, verbose_name='操作人')
    scripts = models.TextField(max_length=10000, null=True, blank=True, verbose_name="操作")
    is_complete = models.BooleanField(default=False, verbose_name="是否已完成")
    remark = models.TextField(max_length=10000, null=True, blank=True, verbose_name=u"备注")

    class Meta:
        db_table = 'daily_report_osa'
        verbose_name = 'AA--日志(OSA)'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pk)
