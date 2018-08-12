from routes import (
    json_response,
    current_user,
    login_required,
    owner_required,
)
from models.todo import Todo
from utils import log, format_time


# 本文件只返回 json 格式的数据, 而不是 html 格式的数据
def all(request):
    """
    返回 json 格式的所有 todo 数据
    """
    u = current_user(request)
    todos = Todo.all(user_id=u.id)
    #处理时间格式
    format_time(todos)

    todos = [todo.to_dict() for todo in todos]
    return json_response(todos)


def add(request):
    '''
    拿到浏览器发送的数据
    用数据创建一个新的 todo  返回给浏览器
    '''
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以用新增加的 dejson 函数来获取解析后的 json 数据
    form = request.dejson()
    u = current_user(request)
    form['user_id'] = u.id
    t = Todo.add(form)
    format_time(t)
    return json_response(t.to_dict())


def delete(request):
    '''
    删除浏览器发送数据对应的 todo
    返回删除成功的信息
    '''
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    d = dict(
        message="成功删除 todo"
    )
    return json_response(d)


def update(request):
    """
    更新 todo 并返回更新后的 todo
    """
    form = request.dejson()
    log('api todo update form', form)
    t = Todo.update(form)
    format_time(t)
    log('update todo:({})'.format(t))
    return json_response(t.to_dict())


def route_dict():
    d = {
        '/api/todo/all': login_required(all),
        '/api/todo/add': login_required(add),
        '/api/todo/delete': login_required(owner_required(delete)),
        '/api/todo/update': login_required(owner_required(update)),
    }
    return d
