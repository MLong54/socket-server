import pymysql

import secret
import config


def comment_table_sql():
    sql = '''
        CREATE TABLE `Comment` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `user_name` VARCHAR(64) NOT NULL,
        `weibo_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
            )'''
    return sql


def session_table_sql():
    sql = '''
        CREATE TABLE `Session` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `session_id` CHAR(16) NOT NULL,
            `user_id` INT NOT NULL,
            `expired_time` INT NOT NULL,
            PRIMARY KEY (`id`)
        )'''
    return sql


def user_table_sql():
    sql = '''
    CREATE TABLE `User` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `username` VARCHAR(45) NOT NULL,
        `password` CHAR(64) NOT NULL,
        `role` ENUM('guest', 'normal') NOT NULL,
        PRIMARY KEY (`id`)
    )'''
    return sql


def weibo_table_sql():
    sql = '''
        CREATE TABLE `Weibo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `content` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `user_name` VARCHAR(64) NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
        )'''
    return sql


def todo_table_sql():
    sql = '''
        CREATE TABLE `Todo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(64) NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''
    return sql


def recreate_table(cursor):
    cursor.execute(user_table_sql())
    cursor.execute(session_table_sql())
    cursor.execute(weibo_table_sql())
    cursor.execute(comment_table_sql())
    cursor.execute(todo_table_sql())


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
