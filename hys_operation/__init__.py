from django.apps import AppConfig
import os
import pymysql
pymysql.install_as_MySQLdb()


default_app_config = 'hys_operation.PrimaryBlogConfig'

VERBOSE_APP_NAME = "本地服务器资源"


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class PrimaryBlogConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME

