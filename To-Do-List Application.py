import json
from datetime import datetime
class Task:
    def _init_(self, title, priority='medium', due_date=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False
    def mark_completed(self):
        self.completed = True
    def to_dict(self):
        return {
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }
    @classmethod
    def from_dict(cls, data):
        task = cls(data['title'], data['priority'], data['due_date'])
        task.completed = data['completed']
        return task
class TaskManager:
    def _init_(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    def add_task(self, title, priority='medium', due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()
    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            status = 'Completed' if task.completed else 'Pending'
            due_date = task.due_date if task.due_date else 'No due date'
            print(f"{i}. {task.title} - {task.priority} - {due_date} - {status}")
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                return [Task.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            return []
def main():
    manager = TaskManager()
    while True:
        print("\nTo-Do List Application")
        print("1. Add task")
        print("2. Remove task")
        print("3. Complete task")
        print("4. List tasks")
        print("5. Exit")
        choice = input("Choose an action (1-5): ")
        if choice == '1':
            title = input("Enter the task title: ")
            priority = input("Enter the task priority (high, medium, low): ").lower()
            due_date = input("Enter the due date (YYYY-MM-DD) or leave empty: ")
            if due_date:
                try:
                    datetime.strptime(due_date, '%Y-%m-%d')
                except ValueError:
                    print("Invalid date format. Task not added.")
                    continue
            manager.add_task(title, priority, due_date or None)
            print("Task added.")
        elif choice == '2':
            try:
                index = int(input("Enter the task index to remove: "))
                manager.remove_task(index)
                print("Task removed.")
            except ValueError:
                print("Invalid index.")
        elif choice == '3':
            try:
                index = int(input("Enter the task index to mark as completed: "))
                manager.mark_task_completed(index)
                print("Task marked as completed.")
            except ValueError:
                print("Invalid index.")
        elif choice == '4':
            manager.list_tasks()
        elif choice == '5':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please choose a valid action.")
if _name_ == '_main_':
    main()
