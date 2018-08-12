import os.path
import random
import json
import time

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.weibo import Weibo
from models.comment import Comment
from models.todo import Todo
from models.session import Session
from models.user import User
from utils import log


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    # 创建读取模板的环境
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class HtmlTemplate:
    '''
    模板类
    提供 render 方法渲染模板
    '''
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def current_user(request):
    print('current_user cookies', request.cookies)
    # 返回当前登录用户， 若未登录则返回游客用户
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        print('session_id', session_id)
        s = Session.one(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one(id=user_id)
            return u
    else:
        return User.guest()


def formatted_header(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=seizer
    """
    header = 'HTTP/1.1 {} OK \r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def html_response(body, headers=None):
    """
    本函数返回 html 格式的 body 数据
    """
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data, headers=None):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    # 注意, content-type 现在是 application/json 而不是 text/html
    # 这个不是很要紧, 因为客户端可以忽略这个
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()


def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': url,
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    # 302 状态码的含义, Location 的作用
    # 注意, 没有 HTTP body 部分
    header = formatted_header(headers, 302)
    r = header + '\r\n'
    return r.encode()


def login_required(route_function):
    """
    装饰器， 要求登录
    """

    def f(request):
        u = current_user(request)
        if u.is_guest():
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('登录用户', route_function)
            return route_function(request)

    return f


def owner_required(route_function):
    """
    所有修改都只能本人才能修改
    权限验证不通过, 用 json 传 message 给前端
    """
    def f(request):
        u = current_user(request)
        # 拿到修改数据对应的 id
        if 'id' in request.query:
            id = request.query['id']
        else:
            form = request.dejson()
            id = form['id']
        # 判断修改数据的类型
        log('id', id)
        if 'todo' in request.path:
            m = Todo.one(id=int(id))
        elif 'weibo' in request.path:
            m = Weibo.one(id=int(id))
        elif 'comment' in request.path:
            m = Comment.one(id=int(id))
        # 判断当前用户与被修改数据的用户是否是同一用户
        log('path', request.path)
        log('member', m)
        if m.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                deny="yes",
                message="owner required",
            )
            return json_response(d)

    return f


def formatted_time(current_time):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(current_time)
    formatted = time.strftime(time_format, localtime)
    return formatted
