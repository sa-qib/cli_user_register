import sqlite3
from utilities.exceptions import *
from authentication.auth import Login
from utilities.validate_input import get_input

class TodoList(Login):
    def __init__(self) -> None:
        super().__init__()
        self.conn = sqlite3.connect('todos.db')
        self.cursor = self.conn.cursor()
        self.user_name = self.userName
        self.user_id = self.cursor.execute('SELECT id FROM users WHERE username = ?', (self.user_name,)).fetchone()[0]


    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id


    def task(self):
        description = input("Add Task: ").strip().title()
        while not description:
            raise EmptyValueError
        return description





    def view(self):
        task_list = []
        self.cursor.execute(
            """SELECT task_name, status, user_id FROM tasks WHERE user_id = ? """, (self.user_id,)
        )
        tasks = self.cursor.fetchall()
        if tasks:
            for id, task in enumerate(sorted(tasks), start=1):
                task, status, user_id = task
                task_list.append({"ID":id, "task":task, "status":status, "user_id":user_id})
            return task_list
        else:
            raise EmptyValueError
    


    def add(self):
        """
        Add a new task to the list.

        Raises:
            ValueAlreadyExistError: If the task already exists.
        """

        task = self.task()
        try:
            exist_tasks = self.view() 
            for exist_task in exist_tasks:
                if exist_task["task"] == task and exist_task["user_id"] == self.user_id:
                    raise ValueAlreadyExistError
        except EmptyValueError:
            pass


        self.cursor.execute(
            """INSERT INTO tasks (user_id, task_name) VALUES (?, ?)""", (self.user_id, task,)
        )
        self.conn.commit()
    


    def remove(self):
        tasks = self.view()
        task_id = int(get_input("remove task by ID: "))
        filter_task = list(filter(lambda i: i["ID"] == task_id, tasks))
         
        try:
            self.cursor.execute(
                """DELETE FROM tasks WHERE task_name = ?""", (filter_task[0]["task"], )
            )
            self.conn.commit()
        except IndexError:
            Display.flash_msg(f"ID with {task_id} not found.")



    def edit(self):
        tasks = self.view()
        task_id = int(get_input("mark task by ID: "))
        filter_task = list(filter(lambda i: i["ID"] == task_id, tasks))[0]
        

        if filter_task:
            match filter_task["status"]:
                case 'pending':
                    self.cursor.execute(
                        """UPDATE tasks SET status = ? WHERE task_name = ?""", ('complete', filter_task["task"], )
                    )
                    self.conn.commit()
                case 'complete':
                    self.cursor.execute(
                        """UPDATE tasks SET status = ? WHERE task_name = ?""", ('pending', filter_task["task"], )
                    )
                    self.conn.commit()

        else:
            raise IndexError(f"ID {task_id} not found.")
    
    
