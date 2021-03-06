from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import quote, unquote
from app import db
from . import auth
from .forms import LoginForm, RegisterForm, AccountEditForm, RoleForm
from ..models import User, School, Role
from ..decorators import permission_required


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('know.push'))
        else:
            flash('密码错误')
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('你已经成功退出帐号')
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    school=School.query.get(form.school.data))
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/register.html', form=form)


@auth.route('/profile/<user_id>')
@login_required
def profile(user_id):
    the_user = User.query.get_or_404(int(user_id))
    return render_template('auth/profile.html', active_flg=['profile'], the_user=the_user)


@auth.route('/account/<user_id>', methods=['GET', 'POST'])
@login_required
def account(user_id):
    the_user = User.query.get_or_404(int(user_id))
    if not current_user.can('user_manage') and the_user.id != current_user.id:
        abort(403)
    form = AccountEditForm(the_user)
    if request.method == 'GET':
        form.set_data()
    if form.validate_on_submit():
        the_user.edit(form.data)
        flash('修改成功')
        return redirect(url_for('.account', user_id=user_id))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/account.html', active_flg=['account'], the_user=the_user, form=form)


@auth.route('/user_del/<user_id>')
@login_required
@permission_required('user_manage')
def user_del(user_id):
    the_user = User.query.get_or_404(int(user_id))
    the_user.delete()
    flash('删除成功')
    return redirect(url_for('.manage'))


@auth.route('/manage/', methods=['GET', 'POST'])
@login_required
@permission_required('user_manage')
def manage():
    if request.method == 'POST':
        words = request.form.get('words')
        if words:
            return redirect(url_for('.user_search', words=quote(words)))
        flash('请输入要查找的内容')
    users = User.query.all()
    return render_template('auth/manage.html', active_flg=['manage'], users=users)


@auth.route('/user_search/<words>', methods=['GET', 'POST'])
@login_required
@permission_required('user_manage')
def user_search(words):
    words = unquote(words)
    if request.method == 'POST':
        words = request.form.get('words')
        if words:
            return redirect(url_for('.user_search', words=quote(words)))
        flash('请输入要查找的内容')
    users = User.search(words)
    return render_template('auth/manage.html', active_flg=['manage'], words=words, users=users)


@auth.route('/role/')
@login_required
@permission_required('user_manage')
def role():
    roles = Role.query.all()
    return render_template('auth/role.html', active_flg=['role'], roles=roles)


@auth.route('/role_add/', methods=['GET', 'POST'])
@login_required
@permission_required('user_manage')
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        Role.add(form.data)
        flash('添加成功')
        return redirect(url_for('.role'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/role_add.html', active_flg=['role'], form=form)


@auth.route('/role_edit/<role_id>', methods=['GET', 'POST'])
@login_required
@permission_required("user_manage")
def role_edit(role_id):
    the_role = Role.query.get_or_404(int(role_id))
    form = RoleForm(the_role)
    if request.method == 'GET':
        form.set_data()
    if form.validate_on_submit():
        the_role.edit(form.data)
        flash('编辑成功')
        return redirect(url_for('.role'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/role_add.html', active_flg=['role'], the_role=the_role, form=form)


@auth.route('/role_del/<role_id>')
@login_required
@permission_required('user_manage')
def role_del(role_id):
    the_role = Role.query.get_or_404(int(role_id))
    the_role.delete()
    flash('删除成功')
    return redirect(url_for('.role'))
