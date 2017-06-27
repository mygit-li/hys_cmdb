#Powered by python 3.5.2 and django 1.11.2

###服务器资源管理
- [1]机房、主机、巡检记录和人员的记录
- [2]不同用户有不同的权限（普通用户查看修改本组服务器信息，经理查看修改所有机器信息，管理员具有所有信息的增删该查功能） 

### 安装
- [1]pip3 install django
- [2]pip3 install pymysql（如果不使用mysql数据库则忽略此步骤）
- [3]mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -uroot -p  mysql（linux服务器下执行，windows自行修改）

### 使用
- [1]资源管理
用户：admin  密码:7ujm8ik,
访问地址： http://192.168.168.250:9000/management/
- [2]资源管理
访问地址： http://192.168.168.250:9000/admin/

### 注：
#### 用户表的“显示权限”字段的意义：
####“普通权限”-->只能看到负责人为本人的服务器；
####“高级权限”-->可以看到负责人所在组的服务器；
