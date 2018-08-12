import pymysql

import secret
import config
from models.session import Session
from models.comment import Comment
from models.weibo import Weibo
from models.todo import Todo
from models.user import User


def recreate_table(cursor):
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(Weibo.sql_create)
    cursor.execute(Comment.sql_create)
    cursor.execute(Todo.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.database_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                config.db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                config.db_name
            )
        )
        cursor.execute('USE `{}`'.format(config.db_name))

        recreate_table(cursor)

    connection.commit()
    connection.close()




if __name__ == '__main__':
    recreate_database()
