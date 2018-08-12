import time

from models.base_model import SQLModel
from models.user import User


class Comment(SQLModel):
    """
    评论类
    """
    sql_create = '''
        CREATE TABLE `comment` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `user_name` VARCHAR(64) NOT NULL,
        `weibo_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
            )'''

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 和 weibo_id 表明拥有它的 user 实例和 weibo 实例
        self.user_id = form['user_id']
        self.user_name = form['user_name']
        self.weibo_id = form['weibo_id']
        self.created_time = form['created_time']
        self.updated_time = form['updated_time']

    @classmethod
    def add(cls, form):
        user = User.one(id=form['user_id'])
        form['user_name'] = user.username
        current_time = int(time.time())
        form['created_time'] = current_time
        form['updated_time'] = current_time
        comment = cls.new(form)
        return comment

    @classmethod
    def update(cls, form):
        id = int(form['id'])
        super().update(
            id=id,
            content=form['content'],
            updated_time=int(time.time())
        )
        comment = cls.one(id=id)
        return comment
