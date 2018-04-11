from flask_script import Manager, Shell
# from flask_migrate import MigrateCommand, Migrate
from app import create_app, db

app = create_app('default')
manager = Manager(app)
# migrate = Migrate(app, db)    # 用于数据库迁移


@manager.command
def deploy():
    """应用程序的初始化配置，主要是数据库基础数据配置"""
    from app.models import School, Role
    db.drop_all()
    db.create_all()
    School.insert_basic_schools()
    Role.insert_basic_roles()
    return '配置成功'


def make_shell_context():
    """
    添加shell中的命令
    :return:
    """
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)    # 用于数据库迁移

if __name__ == '__main__':
    manager.run()
