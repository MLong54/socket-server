import time

from models.base_model import SQLModel
from utils import log


class Session(SQLModel):
    """
    Session 是用来保存 session 的 model
    """
    sql_create = '''
    CREATE TABLE `session` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `session_id` CHAR(16) NOT NULL,
        `user_id` INT NOT NULL,
        `expired_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form['session_id']
        self.user_id = form['user_id']
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        log('expired', result, self.expired_time, now)
        return result
