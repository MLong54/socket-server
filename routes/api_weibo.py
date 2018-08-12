from routes import (
    json_response,
    current_user,
    login_required,
    owner_required,
)
from models.comment import Comment
from models.weibo import Weibo
from utils import log


def weibo_all(request):
    """
    返回 json 格式的所有 weibo 数据
    """
    weibos = Weibo.all_to_dict()
    for weibo in weibos:
        # 获取每条 weibo 对应所有评论
        comments = Comment.all(weibo_id=int(weibo['id']))
        comments_dicts = [comment.to_dict() for comment in comments]

        # 给每个 weibo 对象加上所有评论
        weibo['comments'] = comments_dicts
    return json_response(weibos)


def weibo_add(request):
    '''
    拿到浏览器发送的数据
    用数据创建一个新的 weibo  返回给浏览器
    '''
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以用新增加的 dejson 函数来获取解析后的 json 数据
    form = request.dejson()
    # 创建一个 weibo ，并给 weibo 带上对应的用户名
    u = current_user(request)
    form['user_id'] = u.id
    w = Weibo.add(form)
    return json_response(w.to_dict())


def weibo_delete(request):
    '''
    删除浏览器发送数据对应的 weibo
    返回删除成功的信息
    '''
    weibo_id = int(request.query['id'])
    # 循环遍历该 weibo 所有评论，并删除
    comments = Comment.all(weibo_id=weibo_id)
    for comment in comments:
        Comment.delete(comment.id)
    Weibo.delete(weibo_id)
    d = dict(
        message="成功删除 weibo"
    )
    return json_response(d)


def weibo_update(request):
    """
    更新 weibo 并返回更新后的 weibo
    """
    form = request.dejson()
    log('api weibo update form', form)
    w = Weibo.update(form)
    return json_response(w.to_dict())


def comment_add(request):
    '''
    创建一个 comment
    '''
    form = request.dejson()
    u = current_user(request)
    form['user_id'] = u.id
    c = Comment.add(form)
    return json_response(c.to_dict())


def comment_delete(request):
    """
    用于删除 comment 的路由函数
    """
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除评论"
    )
    return json_response(d)


def comment_update(request):
    """
    用于更新 comment 的路由函数
    """
    form = request.dejson()
    log('api comment update form', form)
    c = Comment.update(form)
    return json_response(c.to_dict())


def weibo_owner_required(route_function):
    """
    所有 weibo 修改都只能本人才能修改
    权限验证不通过, 用 json 传 message 给前端
    """

    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            form = request.json()
            weibo_id = form['id']
        w = Weibo.one(id=int(weibo_id))
        if w.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                deny="yes",
                message="weibo owner required",
            )
            return json_response(d)

    return f


def comment_owner_required(route_function):
    """
    所有 comment 修改都只能本人或者该 comment 对应 weibo 的 user
    权限验证不通过, 用 json 传 message 给前端
    """

    def f(request):
        log('comment_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            form = request.json()
            comment_id = form['id']
        c = Comment.one(id=int(comment_id))
        weibo_id = c.weibo_id
        w = Weibo.one(id=int(weibo_id))
        if c.user_id == u.id or w.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                deny="yes",
                message="comment owner required",
            )
            return json_response(d)

    return f


def route_dict():
    d = {
        '/api/weibo/all': weibo_all,
        '/api/weibo/add': login_required(weibo_add),
        '/api/weibo/delete': login_required(owner_required(weibo_delete)),
        '/api/weibo/update': login_required(owner_required(weibo_update)),
        '/api/comment/add': login_required(comment_add),
        '/api/comment/delete': login_required(owner_required(comment_delete)),
        '/api/comment/update': login_required(owner_required(comment_update)),
    }
    return d



