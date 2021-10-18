import sqlite3
import os

currentDirectory = os.getcwd()
conn = sqlite3.connect('app/base.db')
cursor = conn.cursor()


def get_cursor():
    return cursor


def user_reg(user_id: int):
    user: tuple = (user_id, 0)
    cursor.execute(
        'INSERT INTO Users VALUES(?, ?)', user
    )
    conn.commit()


def is_reg(user_id: int) -> bool:
    base_users_list: list = cursor.execute(
        'SELECT * FROM Users WHERE user_id=?', (user_id,)
    ).fetchall()
    for user in base_users_list:
        if user_id in user:
            return True
        else:
            return False


def get_last_task_id() -> None or int:

    task_id: list = cursor.execute(
        'SELECT task_id FROM Tasks'
    ).fetchall()

    if len(task_id) != 0:
        last_task_id: tuple = task_id.pop()

        for last_id in last_task_id:
            return last_id

    else:
        return None


def new_task(user_id: int, title: str, body: str, task_id: int = 0, status: bool = False):
    task: tuple = (user_id, title, body, status, task_id)
    cursor.execute(
        'INSERT INTO Tasks VALUES(?, ?, ?, ?, ?)', task
    )
    conn.commit()


def get_list_tasks(user_id: int) -> list:
    list_tasks: list = cursor.execute(
        'SELECT title, body, task_id FROM Tasks WHERE user_id=?', (user_id,)
    ).fetchall()
    return list_tasks


def del_task(task_id: int):
    cursor.execute(
        'DELETE FROM Tasks WHERE task_id=?', (task_id,)
    )
    conn.commit()


def edit_task(task_id: int, title: str, body: str):
    cursor.execute(
        'UPDATE Tasks SET title=?, body=? WHERE task_id=?', (title, body, task_id)
    )
    conn.commit()


