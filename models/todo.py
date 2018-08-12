import time

from models.base_model import SQLModel


class Todo(SQLModel):
    """
    Todo 类
    C create 创建数据
    R read 读取数据(继承自父类)
    U update 更新数据
    D delete 删除数据(继承自父类)

    Todo.new() 来创建一个 todo
    """

    sql_create = '''
        CREATE TABLE `todo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.title = form['title']
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form['user_id']
        self.created_time = form['created_time']
        self.updated_time = form['updated_time']

    @classmethod
    def add(cls, form):
        current_time = int(time.time())
        form['created_time'] = current_time
        form['updated_time'] = current_time
        todo = cls.new(form)
        return todo

    @classmethod
    def update(cls, form):
        id = int(form['id'])
        super().update(
            id=id,
            title=form['title'],
            updated_time=int(time.time())
        )
        todo = cls.one(id=id)
        return todo
