import os


class Config(object):
    SECRET_KEY = 'AjkljfiodsLl4398ADFJ90G$#@^5ASFL048509'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改，减少内存使用

    # 自定义配置
    SCHOOLS = ['成都大学']
    PERMISSIONS = [
        ('resource_manage', '知识库文件管理，文件重命名及删除'),
        ('resource_add', '知识库文件添加'),
        ('know_type_manage', '知识库类别管理，目录的添加删除'),
        ('resource_check', '知识库文件审核'),
        ('community_manage', '问答社区管理，问题答案的编辑删除'),
        ('news_manage', '新闻公告管理，新闻公告的发布编辑删除'),
        ('user_manage', '用户管理，权限管理'),
        ('train_manage', '集训系统管理，开关集训、导入小组信息、开关报名、删除等权限'),
        ('train_look', '集训系统查看，进入集训查看各类数据')
    ]
    ROLES = [
        ('普通用户', 'none'),
        ('管理员', 'all'),
        ('知识库文件管理员', ['resource_add', 'resource_manage', 'resource_check', 'know_type_manage'])
    ]
    ADMIN = [
        ('唐柯虎', '329937872@qq.com', 'tang@1013', '成都大学'),
    ]
    TRAIN_FILE_TYPE = {1: '集训题目',
                       2: '参考资料',
                       3: '模型结构',
                       4: '评分标准',
                       5: '评分表',
                       6: '论文',
                       7: '评分结果',
                       8: '总结'}
    FILE_PATH = os.path.join(os.getcwd(), 'app'+os.sep+'static'+os.sep+'know')
    TRAIN_FILE_PATH = os.path.join(os.getcwd(), 'app'+os.sep+'static'+os.sep+'train_files')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/mathmodeling'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:a1!@localhost/mathmodeling'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
