from django.db import models
from django.utils.html import format_html


class UserJob(models.Model):
    """职位表"""
    job_name = models.CharField(max_length=40, verbose_name=u"职位")             # 职位
    department = models.ForeignKey('MachineGroup', verbose_name=u"部门")            # 部门

    class Meta:
        db_table = 'user_job'
        verbose_name = '职位表'
        verbose_name_plural = "职位表"

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
    privilege = models.IntegerField(choices=status_choice, verbose_name='显示权限', db_column='privilege')

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户表'
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.user_name


class City(models.Model):
    """城市分布表"""
    city_name = models.CharField(max_length=40, verbose_name=u"城市名称")         # 城市名称

    class Meta:
        db_table = 'city'
        verbose_name = '城市分布表'
        verbose_name_plural = "城市分布表"

    def __str__(self):
        return self.city_name


class MachineRoom(models.Model):
    """机房信息表"""
    machine_room_name = models.CharField(max_length=40, verbose_name=u"机房名称")                 # 机房名称
    city_belonged = models.ForeignKey('City', verbose_name=u"所属城市")                     # 所属城市id

    class Meta:
        db_table = 'machine_room'
        verbose_name = '机房信息表'
        verbose_name_plural = "机房信息表"

    def __str__(self):
        return self.machine_room_name


class MachineGroup(models.Model):
    """主机所属组"""
    group_name = models.CharField(max_length=40, verbose_name=u"组名称")        # 组名称

    class Meta:
        db_table = 'machine_group'
        verbose_name = '主机属组表'
        verbose_name_plural = "主机属组表"

    def __str__(self):
        return self.group_name


class MachineInfo(models.Model):
    """主机信息表"""
    machine_model = models.CharField(max_length=40, verbose_name=u"型号")        # 型号
    machine_ip = models.CharField(max_length=15, unique=True, verbose_name=u"ip地址")           # ip
    cache = models.CharField(max_length=12, verbose_name=u"内存")                # 内存
    cpu = models.CharField(max_length=4, verbose_name=u"cpu")                   # cpu
    hard_disk = models.CharField(max_length=200, verbose_name=u"磁盘")            # 磁盘大小
    machine_os = models.CharField(max_length=40, verbose_name=u"操作系统")           # 操作系统
    application = models.CharField(max_length=600, verbose_name=u"用途")         # 用途
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
        verbose_name = '主机信息表'
        verbose_name_plural = "主机信息表"

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


class Record(models.Model):
    """巡检记录"""
    go_time = models.DateTimeField(null=True,verbose_name=u"巡检时间")       # 巡检时间
    machine_room_id = models.ForeignKey('MachineRoom', db_column='machine_room_id' ,verbose_name=u"所属机房")  # 机房id
    temperature = models.IntegerField(null=True, verbose_name=u"温度")                        # 温度
    humidity = models.IntegerField(null=True, verbose_name=u"湿度")                 # 湿度
    net = models.CharField(max_length=200, verbose_name=u"网络设备")                         # 网络设备
    server = models.CharField(max_length=200, verbose_name=u"服务器")                         # 服务器
    trouble = models.CharField(max_length=200, verbose_name=u"故障处理")                         # 故障处理
    mark = models.CharField(max_length=200, verbose_name=u"备注")                         # 备注
    act_man = models.ForeignKey('UserInfo', verbose_name=u"巡检人")    # 巡检人

    class Meta:
        db_table = 'record'
        verbose_name = '巡检记录表'
        verbose_name_plural = "巡检记录表"

#    def __str__(self):
#        return self.go_time


class AuthUserGroups(models.Model):
    """人员属组表"""
    user_id = models.IntegerField(verbose_name=u"用户id", db_column='user_id')
    group_id = models.IntegerField(verbose_name=u"属组id", db_column='group_id')

    class Meta:
        db_table = 'auth_user_groups'
        verbose_name = '人员属组关系表'
        verbose_name_plural = verbose_name
        managed = False


class DataPaperStore(models.Model):
    """数据单备案表"""
    project_name = models.CharField(max_length=100, verbose_name=u"项目归属")
    to_mail = models.CharField(max_length=100, verbose_name=u"接收邮箱")
    data_selected = models.CharField(max_length=1000, verbose_name=u"数据选项")
    proposer = models.CharField(max_length=100, verbose_name=u"申请人")
    frequency = models.CharField(max_length=400, verbose_name=u"频率")
    commit_date = models.DateField(null=True, verbose_name=u"申请时间")
    sql = models.TextField(max_length=10000, verbose_name=u"sql语句")
    paper_num = models.CharField(max_length=10, verbose_name=u"备案号")

    class Meta:
        db_table = 'data_paper_store'
        verbose_name = '数据单备案表'
        verbose_name_plural = verbose_name
