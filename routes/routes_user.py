from urllib.parse import unquote_plus

from routes import (
    HtmlTemplate,
    current_user,
    html_response,
    random_string,
    redirect
)
from models.session import Session
from models.user import User
from utils import log


def login(request):
    """
    登录页面的处理函数
    登录成功后设置令牌并返回首页
    登录失败则返回登录页面重新登录
    """
    form = request.form()
    u, result = User.login(form)

    if u.is_guest():
        return redirect('/user/login/view?result={}'.format(result))
    else:
        # session 会话
        # token 令牌
        # 设置一个随机字符串来当令牌使用
        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)
        headers = {
            'Set-Cookie': 'session_id={}; path=/'.format(
                session_id
            )
        }
        return redirect('/', headers)


def login_view(request):
    '''
    登录页面的路由函数, 返回登录页面
    '''
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = HtmlTemplate.render(
        'login.html',
        username=u.username,
        result=result,
    )
    return html_response(body)


def register(request):
    """
    注册页面的处理函数
    注册成功后返回首页
    注册失败则返回注册页面重新注册
    """
    form = request.form()
    u, result = User.register(form)
    log('register post', result)

    if u.is_guest():
        return redirect('/user/register/view?result={}'.format(result))
    else:
        return redirect('/')


def register_view(request):
    '''
    注册页面的路由函数, 返回注册页面
    '''
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = HtmlTemplate.render('register.html', result=result)
    return html_response(body)


# RESTFul
# GET /login
# POST /login
# UPDATE /user
# DELETE /user


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
    }
    return r
