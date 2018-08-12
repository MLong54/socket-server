import time

from models.base_model import SQLModel
from models.comment import Comment
from models.user import User


class Weibo(SQLModel):
    """
    微博类
    C create 创建数据
    R read 读取数据(继承自父类)
    U update 更新数据
    D delete 删除数据(继承自父类)
    comments 方法 返回该微博对应所有评论
    """
    sql_create = '''
        CREATE TABLE `weibo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `user_name` VARCHAR(64) NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
        )'''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form['user_id']
        self.user_name = form['user_name']
        self.created_time = form['created_time']
        self.updated_time = form['updated_time']

    @classmethod
    def add(cls, form):
        user = User.one(id=form['user_id'])
        print('current_user', user.username)
        form['user_name'] = user.username
        current_time = int(time.time())
        form['created_time'] = current_time
        form['updated_time'] = current_time
        print('form', form)
        weibo = cls.new(form)
        return weibo

    @classmethod
    def update(cls, form):
        id = int(form['id'])
        super().update(
            id=id,
            content=form['content'],
            updated_time=int(time.time())
        )
        weibo = cls.one(id=id)
        return weibo

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs
